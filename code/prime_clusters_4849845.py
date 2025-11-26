import sys
import time

# Função para verificar e importar bibliotecas
def check_dependencies():
    missing = []
    try:
        import sympy
    except ImportError:
        missing.append("sympy")
    try:
        import matplotlib
    except ImportError:
        missing.append("matplotlib")
    try:
        import pandas
    except ImportError:
        missing.append("pandas")
    
    if missing:
        print("⚠️  Bibliotecas ausentes detectadas!")
        print(f"Por favor, instale as seguintes bibliotecas para rodar o script: {', '.join(missing)}")
        print(f"Comando sugerido: pip install {' '.join(missing)}")
        sys.exit(1)

check_dependencies()

import sympy
import matplotlib.pyplot as plt
import pandas as pd
from sympy import isprime, primerange

class PrimeClusterFinder:
    def __init__(self, bases=[4849845], num_multipliers=100000):
        self.bases = bases
        self.num_multipliers = num_multipliers
        self.results = {} # Dicionário para armazenar DataFrames por base
        
    def run_for_base(self, base):
        print(f"\n🔍 Iniciando busca por Aglomerados de Primos (Base {base})...")
        print(f"🎯 Analisando os primeiros {self.num_multipliers} multiplicadores primos.\n")
        
        upper_bound = int(self.num_multipliers * 15) # Aumentado para garantir cobertura (n*ln(n))
        primes_iterator = primerange(2, upper_bound)
        
        data = []
        count = 0
        start_time = time.time()
        total_steps = self.num_multipliers
        
        for p in primes_iterator:
            if count >= self.num_multipliers:
                break
            
            center = base * p
            candidates = [center - 4, center - 2, center + 2, center + 4]
            
            primes_found = [n for n in candidates if isprime(n)]
            num_primes = len(primes_found)
            
            status = "Falha"
            if num_primes in [1, 2]:
                status = "Padrão"
            elif num_primes == 3:
                status = "Sucesso Alto"
            elif num_primes == 4:
                status = "QUADRUPLETO"
            
            data.append({
                'Multiplicador_Primo': p,
                'Centro': center,
                'Qtd_Primos': num_primes,
                'Status': status,
                'Primos_Lista': primes_found
            })
            
            count += 1
            if count % 1000 == 0: # Atualizar a cada 1000 para não spammar o terminal
                self._print_progress(count, total_steps, base)
            
        elapsed_time = time.time() - start_time
        print(f"\n✅ Análise da Base {base} concluída em {elapsed_time:.2f} segundos.")
        
        return pd.DataFrame(data)

    def run(self):
        for base in self.bases:
            self.results[base] = self.run_for_base(base)
            
    def _print_progress(self, current, total, base):
        percent = 100 * (current / float(total))
        bar = '█' * int(percent / 2) + '-' * (50 - int(percent / 2))
        sys.stdout.write(f'\r|{bar}| {percent:.1f}% (Base {base})')
        sys.stdout.flush()

    def generate_analysis_html(self):
        # Compare bases
        stats = []
        for base in self.bases:
            df = self.results[base]
            quads = len(df[df['Qtd_Primos'] == 4])
            rate = (quads / len(df)) * 100
            stats.append({'base': base, 'quads': quads, 'rate': rate})
        
        # Sort by rate
        stats.sort(key=lambda x: x['rate'], reverse=True)
        
        if len(stats) >= 1:
            best = stats[0]
            
            analysis_html = f"""
            <div class="card mb-12 bg-gradient-to-r from-slate-800 to-slate-900 text-white shadow-xl">
                <h2 class="text-2xl font-bold mb-4 flex items-center">
                    <span class="text-yellow-400 mr-2">📊</span> Análise da Nova Base (4.8M)
                </h2>
                <p class="mb-4 text-gray-200">
                    Após analisar <strong>{self.num_multipliers:,}</strong> multiplicadores para a base {best['base']}:
                </p>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                    <div class="bg-white/10 p-4 rounded-lg backdrop-blur-sm">
                        <h3 class="font-bold text-lg text-green-400 mb-2">🏆 Desempenho: Base {best['base']}</h3>
                        <ul class="space-y-1 text-sm">
                            <li>Quadrupletos: <strong>{best['quads']}</strong></li>
                            <li>Taxa de Sucesso: <strong>{best['rate']:.4f}%</strong></li>
                        </ul>
                    </div>
                </div>
                <p class="text-sm font-mono bg-black/30 p-3 rounded border border-white/10">
                    💡 Esta base (255255 * 19) visa explorar a região dos Trilhões.
                </p>
            </div>
            """
            return analysis_html
        return ""

    def generate_html_dashboard(self):
        print("\n🌐 Gerando Dashboard HTML...")
        
        analysis_section = self.generate_analysis_html()
        html_sections = ""
        
        # Gerar seções para cada base
        for base in self.bases:
            df = self.results[base]
            quads_df = df[df['Qtd_Primos'] == 4]
            total_quads = len(quads_df)
            success_high = len(df[df['Qtd_Primos'] >= 3])
            success_rate = (success_high / len(df)) * 100
            
            # Dados para o gráfico JS (Sampling para não pesar o HTML se for muito grande)
            # Se tiver mais de 10k pontos, fazemos um sample para o gráfico
            if len(df) > 10000:
                df_plot = df.sample(n=10000, random_state=42).sort_values('Multiplicador_Primo')
            else:
                df_plot = df
                
            x_vals = df_plot['Multiplicador_Primo'].tolist()
            y_vals = df_plot['Qtd_Primos'].tolist()
            
            # Tabela de Quadrupletos (Limitar a 100 para não travar o browser se houver muitos)
            table_rows = ""
            for index, row in quads_df.head(100).iterrows():
                primos_str = ", ".join(map(str, row['Primos_Lista']))
                table_rows += f"""
                <tr class="border-b hover:bg-gray-50">
                    <td class="px-4 py-2 font-bold">{row['Multiplicador_Primo']}</td>
                    <td class="px-4 py-2">{row['Centro']}</td>
                    <td class="px-4 py-2 font-mono text-indigo-700 text-xs">{primos_str}</td>
                </tr>
                """
            
            more_rows_msg = ""
            if len(quads_df) > 100:
                more_rows_msg = f"""
                <div class="p-4 text-center text-gray-500 bg-gray-50 border-t">
                    ... e mais {len(quads_df) - 100} quadrupletos não exibidos na tabela.
                </div>
                """

            html_sections += f"""
            <div class="card mb-12 border-t-4 border-indigo-500">
                <h2 class="text-3xl font-bold mb-6 text-indigo-900">Análise da Base {base}</h2>
                
                <!-- Stats Grid -->
                <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
                    <div class="stat-card bg-gray-50">
                        <p class="text-xs text-gray-500 uppercase">Total Testes</p>
                        <p class="text-2xl font-bold text-gray-800">{len(df):,}</p>
                    </div>
                    <div class="stat-card bg-red-50 border border-red-100">
                        <p class="text-xs text-red-500 uppercase font-bold">Quadrupletos</p>
                        <p class="text-2xl font-bold text-red-600">{total_quads:,}</p>
                    </div>
                    <div class="stat-card bg-blue-50">
                        <p class="text-xs text-blue-500 uppercase">Sucesso (3+)</p>
                        <p class="text-2xl font-bold text-blue-600">{success_high:,}</p>
                    </div>
                    <div class="stat-card bg-green-50">
                        <p class="text-xs text-green-500 uppercase">Eficiência (3+)</p>
                        <p class="text-2xl font-bold text-green-600">{success_rate:.2f}%</p>
                    </div>
                </div>

                <!-- Gráfico -->
                <div id="plot_{base}" style="width:100%;height:400px;" class="mb-8 border rounded bg-white"></div>
                <p class="text-xs text-gray-400 text-center mb-8">* Gráfico exibe amostra de até 10.000 pontos para performance</p>
                
                <!-- Tabela -->
                <div class="mt-8">
                    <h3 class="text-xl font-bold mb-2 text-gray-800 flex items-center">
                        <span class="text-yellow-500 mr-2">★</span> 
                        Quadrupletos Encontrados 
                        <span class="ml-2 text-sm font-normal text-gray-500 bg-gray-200 px-2 py-1 rounded-full">Total: {total_quads}</span>
                    </h3>
                    <div class="overflow-x-auto max-h-96 overflow-y-auto border rounded">
                        <table class="min-w-full table-auto">
                            <thead class="bg-gray-100 sticky top-0">
                                <tr>
                                    <th class="px-4 py-2 text-left">Multiplicador (p)</th>
                                    <th class="px-4 py-2 text-left">Centro ({base}*p)</th>
                                    <th class="px-4 py-2 text-left">Primos Encontrados</th>
                                </tr>
                            </thead>
                            <tbody class="text-sm">
                                {table_rows}
                            </tbody>
                        </table>
                        {more_rows_msg}
                    </div>
                </div>
                
                <script>
                    var trace_{base} = {{
                        x: {x_vals},
                        y: {y_vals},
                        mode: 'markers',
                        type: 'scatter',
                        marker: {{
                            color: {y_vals}.map(y => y === 4 ? '#ef4444' : '#3b82f6'),
                            size: {y_vals}.map(y => y === 4 ? 12 : 4),
                            opacity: 0.6
                        }},
                        text: {x_vals}.map(p => 'Multiplicador: ' + p),
                        name: 'Base {base}'
                    }};
                    var layout_{base} = {{
                        title: 'Distribuição Base {base} (Amostra)',
                        margin: {{t: 40, b: 40, l: 40, r: 20}},
                        xaxis: {{ title: 'Multiplicador Primo' }},
                        yaxis: {{ title: 'Qtd Primos', tickvals: [0,1,2,3,4] }}
                    }};
                    Plotly.newPlot('plot_{base}', [trace_{base}], layout_{base});
                </script>
            </div>
            """

        html_content = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Análise de Aglomerados de Primos - Base 4.8M</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Inter', sans-serif; background-color: #f8fafc; }}
        .card {{ background: white; border-radius: 16px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); padding: 2rem; }}
        .stat-card {{ border-radius: 12px; padding: 1rem; text-align: center; }}
    </style>
</head>
<body class="p-4 md:p-8">
    <div class="max-w-7xl mx-auto">
        <div class="mb-10 text-center">
            <h1 class="text-4xl font-extrabold text-slate-800 mb-2">🔬 Estudo de Base 4.849.845</h1>
            <p class="text-slate-500 text-lg">Analisando a eficiência da base <strong>4.849.845</strong> (255255 * 19)</p>
        </div>
        
        {analysis_section}
        
        {html_sections}
        
        <div class="text-center text-gray-400 text-sm mt-12">
            Gerado automaticamente por Python Script
        </div>
    </div>
</body>
</html>
        """
        
        filename = 'dashboard_base_4849845.html'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"✅ Dashboard gerado: {filename}")

    def generate_full_report_html(self):
        print("\n📄 Gerando Relatório Completo de Quadrupletos...")
        
        html_content = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório Completo - Quadrupletos (Base 4.8M)</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <style>
        body { font-family: 'Inter', sans-serif; background-color: #f8fafc; }
        .table-container { overflow-x: auto; }
    </style>
</head>
<body class="p-8 bg-slate-100">
    <div class="max-w-6xl mx-auto bg-white shadow-lg rounded-lg p-8">
        <h1 class="text-3xl font-bold text-slate-800 mb-2">Relatório Completo de Quadrupletos</h1>
        <p class="text-slate-500 mb-8">Listagem integral de todos os aglomerados encontrados para a Base 4.849.845.</p>
"""
        
        for base in self.bases:
            df = self.results[base]
            quads_df = df[df['Qtd_Primos'] == 4]
            
            html_content += f"""
            <div class="mb-12">
                <h2 class="text-2xl font-bold text-indigo-700 mb-4 border-b pb-2">Base {base} <span class="text-sm text-gray-500 font-normal">({len(quads_df)} encontrados)</span></h2>
                <div class="table-container border rounded-lg overflow-hidden">
                    <table class="min-w-full divide-y divide-gray-200">
                        <thead class="bg-gray-50">
                            <tr>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">#</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Multiplicador (p)</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Centro ({base}*p)</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Primos do Quadrupleto</th>
                            </tr>
                        </thead>
                        <tbody class="bg-white divide-y divide-gray-200">
            """
            
            count = 1
            for index, row in quads_df.iterrows():
                primos_str = ", ".join(map(str, row['Primos_Lista']))
                html_content += f"""
                            <tr class="hover:bg-gray-50">
                                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-400">{count}</td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{row['Multiplicador_Primo']}</td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600">{row['Centro']}</td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm font-mono text-indigo-600">{primos_str}</td>
                            </tr>
                """
                count += 1
                
            html_content += """
                        </tbody>
                    </table>
                </div>
            </div>
            """

        html_content += """
    </div>
</body>
</html>
"""
        filename = 'relatorio_quadrupletos_base_4849845.html'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"✅ Relatório Completo gerado: {filename}")

if __name__ == "__main__":
    # Rodamos para a base 4.849.845 com 100.000 primos
    finder = PrimeClusterFinder(bases=[4849845], num_multipliers=100000)
    finder.run()
    finder.generate_html_dashboard()
    finder.generate_full_report_html()
