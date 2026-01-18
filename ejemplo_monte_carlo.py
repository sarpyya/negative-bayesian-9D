#!/usr/bin/env python3
"""
🔥 EJEMPLO AVANZADO - SIMULACIÓN MONTE CARLO DE HORROR 🔥
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Simula múltiples grafos y encuentra el peor escenario posible.
"""

from bayesian_9d import generar_grafo_9d, analizar_horror, votar_modo, DIMENSIONES_9D
from colorama import Fore, Style, init
import numpy as np
import json

init(autoreset=True)

def simulacion_monte_carlo(n_simulaciones: int = 100):
    """
    Ejecuta N simulaciones y retorna estadísticas.
    """
    print(f"{Fore.YELLOW}🎲 Ejecutando {n_simulaciones} simulaciones Monte Carlo...{Style.RESET_ALL}\n")
    
    resultados = []
    peor_caso = None
    peor_horror = 0
    
    for i in range(n_simulaciones):
        grafo = generar_grafo_9d(seed=i, ramificaciones_por_nodo=5)
        analisis = analizar_horror(grafo, top_n=16)
        
        resultados.append({
            'seed': i,
            'horror_total': analisis['horror_total'],
            'horror_promedio': analisis['horror_promedio']
        })
        
        if analisis['horror_total'] > peor_horror:
            peor_horror = analisis['horror_total']
            peor_caso = {
                'seed': i,
                'analisis': analisis
            }
        
        if (i + 1) % 10 == 0:
            print(f"{Fore.CYAN}  Progreso: {i + 1}/{n_simulaciones}{Style.RESET_ALL}")
    
    # Calcular estadísticas
    horrores = [r['horror_total'] for r in resultados]
    stats = {
        'n_simulaciones': n_simulaciones,
        'horror_min': min(horrores),
        'horror_max': max(horrores),
        'horror_media': np.mean(horrores),
        'horror_mediana': np.median(horrores),
        'horror_std': np.std(horrores),
        'peor_caso': peor_caso
    }
    
    return stats

def print_resultados(stats: dict):
    """Imprime resultados de la simulación"""
    print(f"\n{Fore.RED}{'═' * 70}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}  📊 RESULTADOS SIMULACIÓN MONTE CARLO{Style.RESET_ALL}")
    print(f"{Fore.RED}{'═' * 70}{Style.RESET_ALL}\n")
    
    print(f"{Fore.CYAN}Simulaciones ejecutadas: {Fore.WHITE}{stats['n_simulaciones']}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Horror mínimo: {Fore.WHITE}{stats['horror_min']:,.2f}{Style.RESET_ALL}")
    print(f"{Fore.RED}Horror máximo: {Fore.WHITE}{stats['horror_max']:,.2f}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Horror media: {Fore.WHITE}{stats['horror_media']:,.2f}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Horror mediana: {Fore.WHITE}{stats['horror_mediana']:,.2f}{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}Desviación estándar: {Fore.WHITE}{stats['horror_std']:,.2f}{Style.RESET_ALL}")
    
    print(f"\n{Fore.RED}🔥 PEOR CASO ENCONTRADO{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'─' * 70}{Style.RESET_ALL}")
    
    peor = stats['peor_caso']
    print(f"Seed: {Fore.YELLOW}{peor['seed']}{Style.RESET_ALL}")
    print(f"Horror total: {Fore.RED}{peor['analisis']['horror_total']:,.2f}{Style.RESET_ALL}")
    
    modo_nombre, modo_info = votar_modo(peor['analisis']['horror_total'])
    print(f"\nModo activado: {modo_info['color']}{modo_info['emoji']} {modo_nombre}{Style.RESET_ALL}")
    print(f"{Fore.WHITE}{modo_info['desc']}{Style.RESET_ALL}")
    
    print(f"\n{Fore.RED}Top 3 nodos más horribles del peor caso:{Style.RESET_ALL}")
    for i, nodo in enumerate(peor['analisis']['nodos_mas_horribles'][:3], 1):
        print(f"{Fore.YELLOW}{i}.{Style.RESET_ALL} {Fore.RED}[{nodo['horror']:,.1f}]{Style.RESET_ALL} {nodo['label']}")

if __name__ == "__main__":
    print(f"{Fore.RED}{'═' * 70}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}  🔥 SIMULACIÓN MONTE CARLO - BAYESIAN NEGATIVE 9D 🔥{Style.RESET_ALL}")
    print(f"{Fore.CYAN}  Buscando el peor escenario posible...{Style.RESET_ALL}")
    print(f"{Fore.RED}{'═' * 70}{Style.RESET_ALL}\n")
    
    stats = simulacion_monte_carlo(n_simulaciones=100)
    print_resultados(stats)
    
    # Exportar resultados
    with open('monte_carlo_results.json', 'w', encoding='utf-8') as f:
        # Convertir numpy types a Python nativ para JSON
        stats_serializable = {
            k: float(v) if isinstance(v, (np.floating, np.integer)) else v
            for k, v in stats.items()
        }
        json.dump(stats_serializable, f, indent=2, ensure_ascii=False)
    
    print(f"\n{Fore.GREEN}✅ Resultados guardados en: monte_carlo_results.json{Style.RESET_ALL}")
    print(f"{Fore.RED}{'═' * 70}{Style.RESET_ALL}\n")
