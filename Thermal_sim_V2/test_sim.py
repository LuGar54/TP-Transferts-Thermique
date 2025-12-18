import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from Resistances import *
from Capacitances import *


def load_external_data(file_path):
    """
    Lit le CSV, convertit les dates en heures écoulées et retourne une fonction d'interpolation.
    """
    df = pd.read_csv(file_path, sep=';')
    
    col_time = df.columns[0] # "Time"
    col_temp = df.columns[1] # "Outdoor temperature [deg. C]"
    
    # Conversion du temps
    df[col_time] = pd.to_datetime(df[col_time])
    start_time = df[col_time].iloc[0]
    
    # Calcul du temps écoulé en heures
    time_hours = (df[col_time] - start_time).dt.total_seconds() / 3600.0
    temps = time_hours.values
    temperatures = df[col_temp].values
    
    # interpolateur (fill_value="extrapolate" pour éviter les erreurs aux bornes)
    f_interp = interp1d(temps, temperatures, kind='linear', fill_value="extrapolate")
    
    return f_interp, temps[-1] # Retourne la fonction et la durée max


def get_temp_sol(t_hours, average, amplitude):
    omega = 2 * np.pi / 24.0
    return average + amplitude * np.sin(omega * t_hours)


def compute_Q_flow_net(i, T, right_flow, left_flow):
    """
    Calcule le flux net d'énergie (Advection) dû aux échanges d'air ENTRE zones.
    Q_flow_i = Somme(m_ji * cp * Tj) - Somme(m_ij * cp * Ti)
    """
    Q_gain = 0.0
    Q_loss = 0.0
    
    if i > 0:
        Q_gain += right_flow[i-1] * cp_air * T[i-1]  # Gain de la gauche
        Q_loss += left_flow[i-1] * cp_air * T[i]    # Perte vers la gauche
    
    if i < 5:
        Q_gain += left_flow[i] * cp_air * T[i+1]   # Gain de la droite
        Q_loss += right_flow[i] * cp_air * T[i]  # Perte vers la droite
    
    return Q_gain - Q_loss

def simulation(csv_path, t_end_hours=200):
    temp_ext_interpol, duration_hours = load_external_data(csv_path)
    
    dt = 60.0 # Pas de temps en secondes
    t_end_hours = min(t_end_hours, duration_hours) # On simule le min des 2 (peux pas sim plus que les données)
    steps = int(t_end_hours * 3600 / dt)
    
    Temperatures = np.ones(6) * 15.0 # Température initiale arbitraire (15°C)
    
    # Stockage des résultats
    time_res = []
    temp_res = []
    temp_ext_res = []
    heater_res = []
    
    heaters_state = False # État global des aérothermes
    total_energy_kwh = 0.0
    
    print(f"Lancement de la simulation pour {t_end_hours:.1f} heures...")
    
    for k in range(steps):
        t_sec = k * dt
        t_hour = t_sec / 3600.0
        
        try:
            temp_ext = float(temp_ext_interpol(t_hour))
        except:
            print("erreur temp exterieure interpolation")
            temp_ext = -5.0 # Fallback
            
        temp_sol = get_temp_sol(t_hour, 15, 2)
        
        temp_sensor = (Temperatures[0], Temperatures[5])
        
        # Règles :
        # 1. Arrêt forcé si T_ext > -0.2°C
        # 2. Allumage si T_sensor < 15°C
        # 3. Hystérésis : Arrêt si T_sensor > 45°C (pour éviter cycles courts)
        
        if temp_ext > -0.2:
            heaters_state = False
        elif min(temp_sensor) < 15.0:
            heaters_state = True
        elif max(temp_sensor) > 45.0:
            heaters_state = False
            
        if heaters_state:
            right_flow = m_on_going_right
            left_flow = m_on_going_left
            # Calcul de l'énergie consommée (Puissance * dt) -> Joules -> kWh
            total_energy_kwh += (np.sum(heater_power) * dt) / (3.6e6)
        else:
            right_flow = m_off_going_right
            left_flow = m_off_going_left    
            
        T_new = np.zeros(6)
        
        for i in range(6):
            Q_ext = (temp_ext - Temperatures[i]) / R_plafond_ext
            Q_sol = (temp_sol - Temperatures[i]) / (R_Tbet_Tsol_force[i] if heaters_state else R_Tbet_Tsol_nat[i])
            Q_inf = m_infiltr[i] * cp_air * (temp_ext - Temperatures[i])
            Q_flow = compute_Q_flow_net(i, Temperatures, right_flow, left_flow)
            Q_source = heater_power[i] if heaters_state else 0
            Sum_Q = Q_ext + Q_sol + Q_inf + Q_flow + Q_source
            
            T_new[i] = Temperatures[i] + (dt / C_air_ajuste[i]) * Sum_Q
            
        # Mise à jour du vecteur température
        Temperatures = T_new
        
        # Enregistrement
        if k % 10 == 0: # Pour alléger les graphiques (toutes les 10 min)
            time_res.append(t_hour)
            temp_res.append(Temperatures.copy())
            temp_ext_res.append(temp_ext)
            heater_res.append(1 if heaters_state else 0)
            
    time_res = np.array(time_res)
    temp_res = np.array(temp_res)
    temp_ext_res = np.array(temp_ext_res)
    heater_res = np.array(heater_res)
    
    print(f"\nSimulation terminée.")
    print(f"Consommation énergétique totale : {total_energy_kwh:.2f} kWh")
    
    print("\nTempératures moyennes par zone :")
    for i in range(6):
        print(f"  Zone P{i+1} : {np.mean(temp_res[:, i]):.2f} °C")
        
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True, gridspec_kw={'height_ratios': [3, 1]})
    
    # Graphique Températures
    ax1.plot(time_res, temp_ext_res, 'k--', label="T_ext", alpha=0.7, linewidth=1.5)
    colors = plt.cm.jet(np.linspace(0, 1, 6))
    for i in range(6):
        ax1.plot(time_res, temp_res[:, i], label=f"Zone P{i+1}", color=colors[i])
        
    ax1.axhline(y=3.0, color='gray', linestyle=':', alpha=0.5, label="Seuil Allumage (3°C)")
    ax1.set_ylabel("Température (°C)")
    ax1.set_title("Simulation Thermique Station de Pesée (Modèle R-C Explicite)")
    ax1.legend(loc='upper right', ncol=2)
    ax1.grid(True, alpha=0.3)
    
    # Graphique État Chauffage
    ax2.fill_between(time_res, heater_res, step="pre", color='red', alpha=0.3, label="Chauffage ON")
    ax2.step(time_res, heater_res, where="pre", color='r')
    ax2.set_ylabel("État Aérothermes")
    ax2.set_yticks([0, 1])
    ax2.set_yticklabels(["OFF", "ON"])
    ax2.set_xlabel("Temps (heures)")
    ax2.grid(True)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    filepath = r"Data/Dataset of weighing station temperature measurements.csv"
    simulation(filepath, 2000)