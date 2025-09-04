import files_utils
import json
from typing import Dict, List, Any
from pathlib import Path

def initialize_stats() -> Dict[str, Dict[str, int]]:
    """Inicializa a estrutura de estatísticas vazia"""
    return {
        'pronouns': {},
        'declared_pronouns': {},
        'infered_pronouns': {},
    }

def update_stats(stats: Dict[str, Dict[str, int]], user: Dict[str, Any]) -> None:
    """Atualiza as estatísticas com os dados de um usuário"""
    fields = ['pronouns', 'declared_pronouns', 'infered_pronouns']
    for field in fields:
        value = user.get(field, 'unknown')
        stats[field][value] = stats[field].get(value, 0) + 1

def generate_repo_report(repo_name: str, contributors: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Gera um relatório completo para um repositório"""
    stats = initialize_stats()
    total_contributors = len(contributors)
    
    for contributor in contributors:
        update_stats(stats, contributor)
    
    report = {
        'repo_name': repo_name,
        'total_contributors': total_contributors,
        'stats': {}
    }
    
    for category, values in stats.items():
        report['stats'][category] = {
            value: {
                'count': count,
                'percentage': round((count / total_contributors) * 100, 2) if total_contributors > 0 else 0
            }
            for value, count in values.items()
        }
    
    return report

def save_report(report: Dict[str, Any], output_dir: str = 'reports') -> None:
    """Salva o relatório em um arquivo JSON"""
    Path(output_dir).mkdir(exist_ok=True)
    repo_name = report['repo_name']
    filename = f"{output_dir}/{repo_name}_report.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"Relatório salvo em: {filename}")

def generate_all_reports(repos: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Gera relatórios para todos os repositórios e um consolidado"""
    all_reports = []
    consolidated_stats = initialize_stats()
    total_contributors_all = 0
    
    for repo in repos:
        repo_name = repo['name']
        contributors = files_utils.get_contributor_data(repo_name)
        repo_report = generate_repo_report(repo_name, contributors)
        
        save_report(repo_report)
        all_reports.append(repo_report)
        
        total_contributors_all += repo_report['total_contributors']
        for category in consolidated_stats.keys():
            for value, data in repo_report['stats'][category].items():
                consolidated_stats[category][value] = consolidated_stats[category].get(value, 0) + data['count']
    
    consolidated_report = {
        'total_repos': len(repos),
        'total_contributors': total_contributors_all,
        'stats': {}
    }
    
    for category, values in consolidated_stats.items():
        consolidated_report['stats'][category] = {
            value: {
                'count': count,
                'percentage': round((count / total_contributors_all) * 100, 2) if total_contributors_all > 0 else 0
            }
            for value, count in values.items()
        }
    
    save_report(consolidated_report, 'consolidated_report.json')
    
    return all_reports, consolidated_report

repos = files_utils.get_data('repos.json')

all_reports, consolidated_report = generate_all_reports(repos)

print("\nProcesso concluído!")
print(f"Total de repositórios processados: {len(all_reports)}")
print(f"Relatório consolidado salvo em: consolidated_report.json")
