# Projeto de Análise de Dados Educacionais - PRODITEC

## Sobre o Desenvolvedor

O projeto de análise de dados educacionais do **PRODITEC - Programa de Formação Continuada para Diretores Escolares e Técnicos das Secretarias de Educação** está sendo desenvolvido por **Vitor Lima Menezes**, **servidor da Universidade Federal Fluminense (UFF) e bolsista do projeto**, em parceria com o **Ministério da Educação (MEC)** e a **Universidade Federal de São Carlos (UFSCar)**, e com a coordenação de: **Viviane Merlim Moraes** (Coodenadora Geral do projeto - UFF). 

O projeto está **em constante desenvolvimento**, com atualizações contínuas para aprimorar a análise e visualização dos dados educacionais de 2024 e 2025. O objetivo é fornecer insights estratégicos que auxiliem na gestão da educação, garantindo informações precisas e acessíveis.

## Objetivo do Projeto

O objetivo central é criar uma interface interativa e dinâmica para visualização e análise de dados educacionais, utilizando a biblioteca **Streamlit** para exibição intuitiva. A análise inclui:
- **Mapeamento da distribuição geográfica das escolas** e dos cursistas do PRODITEC.
- **Comparação das taxas de matrícula e evasão** nos diferentes períodos do programa.
- **Análises estatísticas** sobre dependência administrativa, formação dos cursistas e situação acadêmica.
- **Visualização interativa de dados**, utilizando gráficos e mapas interativos.

---

## Tecnologias Utilizadas

O projeto está sendo desenvolvido com tecnologias voltadas para ciência de dados, análise estatística e visualização interativa:

### 1. **Linguagem de Programação: Python**
O núcleo do projeto é construído em **Python**, permitindo manipulação de dados, cálculos estatísticos e geração de visualizações.

### 2. **Framework de Aplicação Web: Streamlit**
A interface do usuário é desenvolvida com **Streamlit**, possibilitando a criação de painéis interativos para apresentação dos dados educacionais.

### 3. **Manipulação de Dados: Pandas**
O projeto faz uso extensivo do **Pandas** para leitura, manipulação e análise dos conjuntos de dados educacionais fornecidos pelo IBGE e pelo PRODITEC.

### 4. **Visualização de Dados: Plotly**
A geração de gráficos interativos é realizada por meio da biblioteca **Plotly**, permitindo a criação de:
- Gráficos de dispersão.
- Boxplots para análise da distribuição dos dados.
- Mapas interativos para exibição geográfica dos cursistas e das escolas atendidas.

### 5. **Geolocalização e Mapas Interativos: Folium e GeoPandas**
A biblioteca **Folium** é utilizada para a criação de mapas interativos, permitindo a visualização detalhada da distribuição das escolas e cursistas por estado e município. Já o **GeoPandas** é empregado para a manipulação avançada de dados geoespaciais, possibilitando análises mais aprofundadas sobre a cobertura do PRODITEC e a relação entre dados geográficos e educacionais.

### 6. **Streamlit Components**
Para exibição de arquivos HTML diretamente na interface Streamlit, é utilizada a biblioteca `streamlit.components.v1`.

---

## Conclusão

Este projeto está **em constante evolução**, com aprimoramentos contínuos na análise dos dados e na experiência do usuário. O uso de ferramentas como **Streamlit, Pandas, Plotly, Folium e GeoPandas** possibilita uma abordagem interativa e acessível, proporcionando um panorama detalhado da realidade educacional dos cursistas do **PRODITEC**. À medida que novos dados são incorporados, a plataforma se tornará ainda mais robusta, garantindo uma visão cada vez mais precisa e estratégica da formação continuada no Brasil.
