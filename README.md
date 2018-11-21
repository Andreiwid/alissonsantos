# Método de catalogação de portais de dados abertos a partir de URLs indexadas no Common Crawl #
<p>       Este trabalho objetivou desenvolver um método de  catalogação de URLs de portais de dados abertos governamentais a partir  da base de dados do 
 Common Crawl (https://commoncrawl.org), que é um projeto livre e aberto para indexação de dados de toda a internet. Foram empregadas técnicas de data science e web scraping, considerando  os conceitos e princípios de dados abertos governamentais, Lei de Acesso à Informação brasileira, plataformas de dados abertos e um trabalho seminal onde se desenvolveu uma forma de identificar algumas destas plataformas. Como resultado obtido, foi possível observar a distribuição geográfica dos portais de dados identificados e a especificação da plataforma utilizada. A contribuição deste trabalho  se deu com um método que poderá ser reproduzido em grande escala e executado repetidamente, de modo a servir de base para construção de um repositório central e atualizável com endereços virtuais (URLs) dos portais de dados abertos em utilização. </p>
<p>
 
 ### Objetivo geral: <br /> 
* O objetivo deste trabalho foi desenvolver um método de catalogação de portais de dados abertos a partir de URLs indexadas no Common Crawl.<br />
  <br />
 ### Objetivos específicos: <br />
  * Desenvolver um método de acesso aos dados do Common Crawl;<br />
  * Desenvolver um método que implemente e use  as assinaturas de identificação das quatro plataformas de dados abertos consideradas;<br />
  * Modelar um banco de dados para a catalogação;<br />
  * Definir um modelo para automatizar o processo para funcionar em larga escala e repetidamente usando como parâmetros as URLs que tenham o sufixo .gov ou sinônimos do mesmo utilizados em outros idiomas/culturas.<br />
</p>

<p>
 # Instruções: <br />
 ## Este projeto esta dividido em duas partes
 </p>
 <p>
 ### A primeira onde é feito o download e rastreio de URLs com a sigla .gov na base de dados do Common Crawl.
 </p>
 Para rodar a primeira parte após o download do projeto vá via terminal até o arquivo start.py que esta na raiz do projeto e digite o comando: python start.py
 <br />
 
 
 e a segunda que é analisado se as URLs .gov respondem a alguma assinatura, (para mais detalhes por favor leia o pdf do TCC).  
 
 
 
</p>
