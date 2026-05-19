import pandas as pd
import json
import glob
import os

def json_to_spreadsheet(json_data, filename):
    """
    Converte o JSON de pronomes em uma planilha estruturada
    """
    # Extrair dados básicos - usar filename como fallback
    repo_name = json_data.get('repo_name', filename)
    total_contributors = json_data.get('total_contributors', 0)
    
    # Criar lista para armazenar os dados
    rows = []
    
    # Processar cada categoria de pronomes
    stats = json_data.get('stats', {})
    for category, pronouns_data in stats.items():
        for pronoun, details in pronouns_data.items():
            rows.append({
                'repositorio': repo_name,
                'total_contributors': total_contributors,
                'categoria': category,
                'pronome': pronoun,
                'contagem': details['count'],
                'percentual': details['percentage']
            })
    
    return rows

def process_all_reports():
    """
    Processa todos os arquivos JSON no diretório ./reports
    """
    # Caminho para os arquivos JSON
    reports_dir = './reports'
    json_pattern = os.path.join(reports_dir, '*.json')
    
    # Encontrar todos os arquivos JSON
    json_files = glob.glob(json_pattern)
    
    if not json_files:
        print(f"Nenhum arquivo JSON encontrado em {reports_dir}!")
        return None
    
    print(f"Encontrados {len(json_files)} arquivos JSON em ./reports")
    
    all_data = []
    
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
            
            # Extrair nome do arquivo sem extensão para usar como fallback
            filename = os.path.splitext(os.path.basename(json_file))[0]
            
            # Processar dados do JSON
            rows = json_to_spreadsheet(json_data, filename)
            all_data.extend(rows)
            
            print(f"✓ Processado: {filename}")
            
        except Exception as e:
            print(f"✗ Erro ao processar {json_file}: {e}")
    
    if not all_data:
        print("Nenhum dado foi processado.")
        return None
    
    # Criar DataFrame consolidado
    df = pd.DataFrame(all_data)
    
    # Salvar como CSV no diretório atual
    output_file = 'pronouns_analysis_consolidada.csv'
    df.to_csv(output_file, index=False, float_format='%.2f')
    
    print(f"\n✅ Planilha consolidada criada com sucesso: {output_file}")
    print(f"📊 Total de repositórios: {df['repositorio'].nunique()}")
    print(f"📈 Total de registros: {len(df)}")
    
    # Mostrar preview dos dados
    print("\n📋 Preview dos dados:")
    print(df.head(10))
    
    return df

if __name__ == "__main__":
    # Verificar se o diretório existe
    if not os.path.exists('./reports'):
        print("❌ Diretório './reports' não encontrado!")
        print("Certifique-se de que o diretório existe e contém arquivos JSON")
    else:
        # Processar todos os relatórios
        df = process_all_reports()
        
        if df is not None:
            # Estatísticas básicas
            print(f"\n📊 Estatísticas finais:")
            print(f"Repositórios únicos: {df['repositorio'].nunique()}")
            print(f"Categorias únicas: {df['categoria'].nunique()}")
            print(f"Pronomes únicos: {df['pronome'].nunique()}")