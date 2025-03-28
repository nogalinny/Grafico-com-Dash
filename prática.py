import plotly.express as px  # Biblioteca para criar gráficos interativos
import pandas as pd  # Biblioteca para manipulação de dados
from dash import Dash, html, dcc  # Importa o Dash para criar a interface web

# Função para criar os gráficos
def cria_graficos(df):
    # Cria um histograma para visualizar a distribuição das notas dos produtos
    fig1 = px.histogram(df, x='Nota', nbins=10, title='Distribuição das Notas dos Produtos')
    
    # Cria um histograma para visualizar a distribuição do número de avaliações
    fig2 = px.histogram(df, x='N_Avaliações', nbins=20, title='Distribuição do Número de Avaliações')
    
    # Cria um gráfico de dispersão hexagonal para analisar relação entre avaliações e notas
    fig3 = px.density_heatmap(df, x='N_Avaliações', y='Nota', title='Produtos avaliados e suas notas', marginal_x='histogram', marginal_y='histogram')
    
    # Calcula a matriz de correlação entre variáveis numéricas
    df_corr = df[['Desconto', 'N_Avaliações', 'Preço', 'Qtd_Vendidos_Cod']].corr()
    
    # Cria um mapa de calor da correlação
    fig4 = px.imshow(df_corr, text_auto=True, title='Mapa de Calor - Correlação entre Variáveis')
    
    # Cria um gráfico de barras para visualizar a quantidade vendida por temporada
    fig5 = px.bar(df, x='Temporada_Cod', y='Qtd_Vendidos_Cod', title='Quantidade Vendida na Temporada', color_discrete_sequence=['#90ee70'])
    
    # Agrupa os dados por gênero e soma a quantidade vendida
    genero_counts = df.groupby('Gênero')['Qtd_Vendidos_Cod'].sum().reset_index()
    
    # Cria um gráfico de pizza para visualizar a quantidade vendida por gênero
    fig6 = px.pie(genero_counts, names='Gênero', values='Qtd_Vendidos_Cod', title='Quantidade de Produtos Vendidos por Gênero')
    
    # Cria um gráfico de densidade para visualizar a distribuição de preços
    fig7 = px.density_contour(df, x='Preço_MinMax', title='Densidade de Preços')
    
    # Cria um gráfico de dispersão para analisar a relação entre quantidade vendida e desconto
    fig8 = px.scatter(df, x='Qtd_Vendidos_Cod', y='Desconto', title='Regressão de Quantidade Vendida pelo Desconto')
    
    return fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8  # Retorna todos os gráficos

# Função para criar o aplicativo Dash
def criar_app(df):  
    app = Dash(__name__)  # Inicializa o aplicativo Dash
    fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8 = cria_graficos(df)  # Obtém os gráficos
    
    # Define o layout do aplicativo
    app.layout = html.Div([
        dcc.Graph(figure=fig1),  # Exibe o gráfico 1
        dcc.Graph(figure=fig2),  # Exibe o gráfico 2
        dcc.Graph(figure=fig3),  # Exibe o gráfico 3
        dcc.Graph(figure=fig4),  # Exibe o gráfico 4
        dcc.Graph(figure=fig5),  # Exibe o gráfico 5
        dcc.Graph(figure=fig6),  # Exibe o gráfico 6
        dcc.Graph(figure=fig7),  # Exibe o gráfico 7
        dcc.Graph(figure=fig8)   # Exibe o gráfico 8
    ])
    
    return app  # Retorna o aplicativo criado

# Carrega os dados do arquivo Excel
df = pd.read_excel('ecommerce_estatistica.xlsx')

# Executa o aplicativo se o script for rodado diretamente
if __name__ == '__main__':
    app = criar_app(df)  # Cria o app
    app.run(debug=True, port=8050)  # Inicia o servidor na porta 8050