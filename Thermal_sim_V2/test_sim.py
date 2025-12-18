import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
# import json
from Resistances import *
from Capacitances import *

# --- 1. PARAMÈTRES ET CONSTANTES (Intégration du JSON) ---
# PARAMS = {
#   "geometrie": {
#     "epaisseur_plaque": 0.009525, "epaisseur_asphalte": 0.08, "epaisseur_ciment": 0.4, "epaisseur_isolant": 0.1,
#     "longueur_puits": 26.1, "largeur_puits": 3.7, "hauteur_puits": 1.7,
#     "A_ciment_p1": 35.2446875, "A_ciment_p2": 28.9546875, "A_ciment_p3": 28.9546875,
#     "A_ciment_p4": 34.7456250, "A_ciment_p5": 34.7456250, "A_ciment_p6": 35.2446875,
#     "A_plaque_p1": 15.0890625, "A_plaque_p2": 15.0890625, "A_plaque_p3": 15.0890625,
#     "A_plaque_p4": 18.1068750, "A_plaque_p5": 18.1068750, "A_plaque_p6": 15.0890625
#   },
#   "proprietes": {
#     "k_acier": 50, "k_ciment": 1.4, "k_isolant": 0.03, "k_asphalte": 0.8,
#     "cp_air": 1000, "h_int": 10, "h_ext": 30, "rho_air": 1.2
#   },
#   "infiltration": {
#     "gap_1": 0.05107, "gap_2": 0.07930, "gap_3": -0.59202,
#     "gap_4": -0.1498, "gap_5": -0.04247, "gap_front": 0.02483, "gap_back": 0.02567
#   },
#   "flow_heaterON": {
#     "f12": 0.2381, "f21": 0.4438, "f23": 0.3268, "f32": 0.7042,
#     "f34": 0.2646, "f43": 0.5915, "f45": 0.1988, "f54": 0.2915,
#     "f56": 0.4694, "f65": 0.4070
#   },
#   "flow_heaterOFF": {
#     "f12": 0.04113, "f21": 0.06844, "f23": 0.0529, "f32": 0.09304,
#     "f34": 0.05121, "f43": 0.10386, "f45": 0.04163, "f54": 0.08528,
#     "f56": 0.03718, "f65": 0.05788
#   },
#   "chauffage": {
#     "p1": 10000, "p2": 15000, "p3": 10000, "p4": 7500, "p5": 7500, "p6": 10000
#   },
#   "temperature_sol": {
#     "T_mean": 15, "A": 0, "t0": 0.0, "phi": 0.0
#   },
#   "capacitance_thermique": {
#     "C1": 600781.6875, "C2": 607081.6875, "C3": 607801.6875,
#     "C4": 669380.025,  "C5": 669380.025,  "C6": 607810.6875
#   }
# }

# --- 2. GESTION DES DONNÉES D'ENTRÉE ---

def load_external_data(file_path):
    """
    Lit le CSV, convertit les dates en heures écoulées et retourne une fonction d'interpolation.
    """
    try:
        df = pd.read_csv(file_path, sep=';')
        
        # Identification des colonnes (basé sur le fichier fourni)
        col_time = df.columns[0] # "Time"
        col_temp = df.columns[1] # "Outdoor temperature [deg. C]"
        
        # Conversion du temps
        df[col_time] = pd.to_datetime(df[col_time])
        start_time = df[col_time].iloc[0]
        
        # Calcul du temps écoulé en heures
        time_hours = (df[col_time] - start_time).dt.total_seconds() / 3600.0
        temps = time_hours.values
        temperatures = df[col_temp].values
        
        # Création de l'interpolateur (fill_value="extrapolate" pour éviter les erreurs aux bornes)
        f_interp = interp1d(temps, temperatures, kind='linear', fill_value="extrapolate")
        
        return f_interp, temps[-1] # Retourne la fonction et la durée max
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier CSV: {e}")
        return None, 0

# --- 3. MODÉLISATION PHYSIQUE ---

def get_temp_sol(t_hours, average, amplitude):
    omega = 2 * np.pi / 24.0
    return average + amplitude * np.sin(omega * t_hours)

# def compute_resistances(geom, prop):
#     """
#     Calcul des R_ext (vers l'air via plaque+asphalte) et R_sol (vers le sol via ciment+isolant)
#     """
#     R_ext = np.zeros(6)
#     R_sol = np.zeros(6)
    
#     # R = L / (k*A)  et R_conv = 1 / (h*A)
#     for i in range(6):
#         idx = i + 1
#         Ap = geom[f"A_plaque_p{idx}"]
#         Ac = geom[f"A_ciment_p{idx}"]
        
#         # Résistance équivalente vers l'extérieur (Série : Conv_int + Acier + Asphalte + Conv_ext)
#         R_ext[i] = (1 / (prop["h_int"] * Ap)) + \
#                    (geom["epaisseur_plaque"] / (prop["k_acier"] * Ap)) + \
#                    (geom["epaisseur_asphalte"] / (prop["k_asphalte"] * Ap)) + \
#                    (1 / (prop["h_ext"] * Ap))
        
#         # Résistance équivalente vers le sol (Série : Conv_int + Ciment + Isolant)
#         # Note : On néglige souvent la convection côté sol car contact solide, 
#         # mais le modèle test.py inclut h_int. On suit la logique du modèle R-C.
#         R_sol[i] = (1 / (prop["h_int"] * Ac)) + \
#                    (geom["epaisseur_ciment"] / (prop["k_ciment"] * Ac)) + \
#                    (geom["epaisseur_isolant"] / (prop["k_isolant"] * Ac))
                   
#     return R_ext, R_sol

# def get_infiltration_masses(inf_data):
#     """Calcule le débit massique d'infiltration par zone"""
#     m = np.zeros(6)
#     # Logique d'infiltration (approximation basée sur les gaps gauche/droite)
#     m[0] = 0.5 * inf_data["gap_1"] + inf_data["gap_front"]
#     m[1] = 0.5 * (inf_data["gap_1"] + inf_data["gap_2"])
#     m[2] = 0.5 * (inf_data["gap_2"] + inf_data["gap_3"])
#     m[3] = 0.5 * (inf_data["gap_3"] + inf_data["gap_4"])
#     m[4] = 0.5 * (inf_data["gap_4"] + inf_data["gap_5"])
#     m[5] = 0.5 * inf_data["gap_5"] + inf_data["gap_back"]
#     return np.abs(m) # On prend la valeur absolue pour le débit entrant

def compute_Q_flow_net(i, T, right_flow, left_flow):
    """
    Calcule le flux net d'énergie (Advection) dû aux échanges d'air ENTRE zones.
    Q_flow_i = Somme(m_ji * cp * Tj) - Somme(m_ij * cp * Ti)
    """
    # idx = i + 1 # Zones numérotées 1 à 6
    Q_gain = 0.0
    Q_loss = 0.0
    
    if i > 0:
        Q_gain += right_flow[i-1] * cp_air * T[i-1]  # Gain de la gauche
        Q_loss += left_flow[i-1] * cp_air * T[i]    # Perte vers la gauche
    
    if i < 5:
        Q_gain += left_flow[i] * cp_air * T[i+1]   # Gain de la droite
        Q_loss += right_flow[i] * cp_air * T[i]  # Perte vers la droite
    
    # Parcourir tous les flux définis (ex: "f12" signifie de 1 vers 2)
    # for key, val in flows.items():
    #     src = int(key[1]) # ex: '1'
    #     dst = int(key[2]) # ex: '2'
        
    #     mdot_cp = val * cp_air # Débit * Cp
        
    #     if dst == idx:
    #         # Gain venant de src (T_voisin)
    #         # T est indexé 0..5, donc src-1
    #         Q_gain += mdot_cp * T[src-1]
        
    #     if src == idx:
    #         # Perte partant de moi (T_i) vers dst
    #         Q_loss += mdot_cp * T[i]
            
    return Q_gain - Q_loss

def simulation(csv_path, t_end_hours=200):
    temp_ext_interpol, duration_hours = load_external_data(csv_path)
    if temp_ext_interpol is None:
        print("Pas de fichier de données, cancel la simulation.")
        return
    
    # geom = PARAMS["geometrie"]
    # prop = PARAMS["proprietes"]
    # caps = PARAMS["capacitance_thermique"]
    # chauff = PARAMS["chauffage"]
    
    # C = np.array([caps[f"C{i+1}"] for i in range(6)])
    
    # P_heater = np.array([chauff[f"p{i+1}"] for i in range(6)])
    
    # R_ext, R_sol = compute_resistances(geom, prop)
    # m_inf = get_infiltration_masses(PARAMS["infiltration"])
    
    # 3. Paramètres de simulation
    dt = 60.0 # Pas de temps en secondes
    t_end_hours = min(t_end_hours, duration_hours) # On simule 48h ou la durée du fichier
    steps = int(t_end_hours * 3600 / dt)
    
    # Conditions initiales
    Temperatures = np.ones(6) * 15.0 # Température initiale arbitraire (15°C)
    
    # Stockage des résultats
    time_res = []
    T_res = []     # Températures zones
    Text_res = []  # Température extérieure
    Heater_res = [] # État chauffage (0 ou 1)
    
    heaters_state = False # État global des aérothermes
    total_energy_kwh = 0.0
    
    print(f"Lancement de la simulation pour {t_end_hours:.1f} heures...")
    
    # 4. Boucle Temporelle (Explicite)
    for k in range(steps):
        t_sec = k * dt
        t_hour = t_sec / 3600.0
        
        # --- A. Conditions aux limites ---
        # Température extérieure (interpolée)
        try:
            temp_ext = float(temp_ext_interpol(t_hour))
        except:
            print("erreur temp exterieure interpolation")
            temp_ext = -5.0 # Fallback
            
        # Température sol (harmonique)
        temp_sol = get_temp_sol(t_hour, 15, 2)
        
        # --- B. Logique de Contrôle ---
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
            
        # Sélection des débits et puissances
        if heaters_state:
            # flows = PARAMS["flow_heaterON"]
            right_flow = m_on_going_right
            left_flow = m_on_going_left
            # Calcul de l'énergie consommée (Puissance * dt) -> Joules -> kWh
            total_energy_kwh += (np.sum(heater_power) * dt) / (3.6e6)
        else:
            # flows = PARAMS["flow_heaterOFF"]
            right_flow = m_off_going_right
            left_flow = m_off_going_left    
            
        # --- C. Calcul des Flux (Bilan explicite) ---
        T_new = np.zeros(6)
        
        for i in range(6):
            # 1. Pertes vers l'extérieur (Conduction/Convection)
            # Flux = (Text - Ti) / R
            Q_ext = (temp_ext - Temperatures[i]) / R_plafond_ext
            
            # 2. Pertes vers le sol
            Q_sol = (temp_sol - Temperatures[i]) / (R_Tbet_Tsol_force[i] if heaters_state else R_Tbet_Tsol_nat[i])
            
            # 3. Infiltration (Air extérieur entrant)
            # Q = m * cp * (Text - Ti)
            Q_inf = m_infiltr[i] * cp_air * (temp_ext - Temperatures[i])
            
            # 4. Échanges entre zones (Advection)
            Q_flow = compute_Q_flow_net(i, Temperatures, right_flow, left_flow)
            
            # 5. Apport Aérotherme
            Q_source = heater_power[i] if heaters_state else 0
            
            # Somme des flux
            Sum_Q = Q_ext + Q_sol + Q_inf + Q_flow + Q_source
            
            # Mise à jour Euler Explicite : Ti(t+1) = Ti(t) + (dt/C) * Sum_Q
            T_new[i] = Temperatures[i] + (dt / C_air_ajuste[i]) * Sum_Q
            
        # Mise à jour du vecteur température
        Temperatures = T_new
        
        # Enregistrement
        if k % 10 == 0: # Pour alléger les graphiques (toutes les 10 min)
            time_res.append(t_hour)
            T_res.append(Temperatures.copy())
            Text_res.append(temp_ext)
            Heater_res.append(1 if heaters_state else 0)
            
    # --- 5. RÉSULTATS ET GRAPHIQUES ---
    time_res = np.array(time_res)
    T_res = np.array(T_res)
    Text_res = np.array(Text_res)
    Heater_res = np.array(Heater_res)
    
    print(f"\nSimulation terminée.")
    print(f"Consommation énergétique totale : {total_energy_kwh:.2f} kWh")
    
    # Statistiques
    print("\nTempératures moyennes par zone :")
    for i in range(6):
        print(f"  Zone P{i+1} : {np.mean(T_res[:, i]):.2f} °C")
        
    # Création du graphique
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True, gridspec_kw={'height_ratios': [3, 1]})
    
    # Graphique Températures
    ax1.plot(time_res, Text_res, 'k--', label="T_ext", alpha=0.7, linewidth=1.5)
    colors = plt.cm.jet(np.linspace(0, 1, 6))
    for i in range(6):
        ax1.plot(time_res, T_res[:, i], label=f"Zone P{i+1}", color=colors[i])
        
    ax1.axhline(y=3.0, color='gray', linestyle=':', alpha=0.5, label="Seuil Allumage (3°C)")
    ax1.set_ylabel("Température (°C)")
    ax1.set_title("Simulation Thermique Station de Pesée (Modèle R-C Explicite)")
    ax1.legend(loc='upper right', ncol=2)
    ax1.grid(True, alpha=0.3)
    
    # Graphique État Chauffage
    ax2.fill_between(time_res, Heater_res, step="pre", color='red', alpha=0.3, label="Chauffage ON")
    ax2.step(time_res, Heater_res, where="pre", color='r')
    ax2.set_ylabel("État Aérothermes")
    ax2.set_yticks([0, 1])
    ax2.set_yticklabels(["OFF", "ON"])
    ax2.set_xlabel("Temps (heures)")
    ax2.grid(True)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Nom du fichier CSV fourni
    filepath = r"Data/Dataset of weighing station temperature measurements.csv"
    simulation(filepath, 300)