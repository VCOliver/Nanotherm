# Nanotherm - A Evolução do Projeto SOFIA

O Nanotherm representa a modernização e o aprimoramento do SOFIA (Software of Intensive Ablation), um equipamento de ablação hepática por radiofrequência (RFA) originalmente desenvolvido em uma parceria acadêmica entre a Universidade de Brasília (UnB) e o Ministério da Saúde. Agora, o projeto é liderado e impulsionado pela startup Metala.

Este projeto visa atualizar a tecnologia do SOFIA para padrões mais atuais, corrigir limitações do sistema original e introduzir melhorias significativas para aumentar a eficácia, segurança e acessibilidade do tratamento de tumores hepáticos, em especial o Carcinoma Hepatocelular (CHC).

## Índice

 - Sobre o Projeto

    - O Legado do SOFIA

    - O Desafio: Limitações da RFA e o Fenômeno de Roll-off

    - A Solução: Nanotherm

 - Principais Funcionalidades e Melhorias

 - Tecnologias Utilizadas

 - Status do Projeto

 - Como Contribuir

 - Desenvolvido por Metala

 - Licença

## Sobre o Projeto

### O Legado do SOFIA

O projeto **SOFIA** nasceu como uma iniciativa para desenvolver uma tecnologia nacional de baixo custo para o tratamento de câncer de fígado, visando atender a uma demanda crítica do Sistema Único de Saúde (SUS) e fomentar a inovação no Complexo Industrial da Saúde no Brasil.


### O Desafio: Limitações da RFA e o Fenômeno de *Roll-off*

A técnica de Ablação por Radiofrequência (RFA) é altamente eficaz para tumores de até 3 cm de diâmetro. No entanto, sua eficiência é limitada em tumores maiores. Um dos principais fatores limitantes é o fenômeno de ***roll-off***: um aumento súbito na impedância do tecido próximo ao eletrodo, causado pela carbonização e vaporização celular. Quando o *roll-off* ocorre, a entrega de energia ao tumor é interrompida, limitando o crescimento da zona de necrose.

### A Solução: Nanotherm

O **Nanotherm** surge como a resposta a esses desafios. Trata-se de uma modernização completa do SOFIA, com foco em superar as limitações da RFA convencional. O objetivo é desenvolver protocolos de operação mais inteligentes e eficientes para maximizar a zona de necrose, permitindo o tratamento seguro de tumores maiores.

As principais frentes de aprimoramento incluem:

1. **Controle Avançado de Energia:** Implementação de novos protocolos que utilizam formas de onda pulsadas (quadrada, triangular) para uma entrega de energia mais controlada e gradual.

2. **Gestão do *Roll-off*:** Desenvolvimento de técnicas, como a infusão de soluções salinas refrigeradas, para retardar o *roll-off* e permitir uma aplicação de energia mais prolongada.

3. **Desenvolvimento de Eletrodos:** Criação e teste de novos eletrodos, como o modelo "guarda-chuva" de NiTi (Níquel-Titânio), projetados para otimizar a distribuição da corrente.

4. **Modernização de Hardware e Software:** Atualização da plataforma de hardware e da interface de software para garantir maior precisão, segurança e usabilidade.

## Principais Funcionalidades e Melhorias

O Nanotherm aprimora o sistema original com funcionalidades focadas em eficácia e controle, garantindo um procedimento de ablação mais seguro e eficiente.

 - **Protocolos de Energia Avançados:** Utiliza formas de onda pulsadas e modelos matemáticos preditivos para otimizar a entrega de energia e prever a ocorrência de *roll-off*.

 - **Monitoramento em Tempo Real:** Interface que exibe os parâmetros vitais do procedimento (potência, impedância, temperatura).

 - **Eletrodos Otimizados:** Emprega eletrodos expansíveis de NiTi para maximizar o contato e a eficácia da ablação.

Tecnologias Utilizadas

 - Hardware:

    - Gerador de RF com controle de potência (até 50W, ~400-550 kHz).

    - Plataforma de processamento: Raspberry Pi 4B (prototipagem inicial) e MCU dedicado para operação em tempo real (versão final).

    - Conversores, circuitos de potência e ganho, e também de medição de impedância, tensão e corrente.

    - Eletrodos de NiTi com microsoldagem a laser.

 - Software:

    - Linguagem de Programação: Python 3.12 ou posterior

    - Interface Gráfica (GUI): PyQt5 or Tkinter

    - Modelagem e Análise de Dados: Python Pandas

## Status do Projeto

O projeto Nanotherm encontra-se em fase de desenvolvimento e validação. As atividades atuais incluem:

 - Testes in vitro para validar os novos protocolos e o desempenho do eletrodo.

 - Refinamento dos algoritmos de controle e do modelo matemático.

 - Aprimoramento da interface de usuário e integração final com o hardware.

## Como Participar

Este é um projeto desenvolvido comercialmente pela **Metala**. Para oportunidades de parceria ou contribuição, por favor, entre em contato através do nosso email oficial: metala.nanofluidos@gmail.com.

## Desenvolvido por Metala

O Nanotherm é um projeto de inovação liderado pela Metala, uma startup brasileira que nasceu da paixão por inovação científica e da busca por soluções disruptivas para os desafios da medicina moderna. Fundada por um grupo de especialistas em nanotecnologia, biomedicina, engenharia eletrônica e engenharia biomédica, a Metala combina ciência de ponta com o compromisso de melhorar a qualidade de vida dos pacientes e transformar o futuro do tratamento de câncer. 

Para saber mais sobre a Metala e nossos outros projetos, visite: https://metalanano.com/

## Licença

Este projeto é distribuído sob a Licença Apache 2.0.

**NOTICE**

Copyright 2024 Metala

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Este projeto contém trabalhos derivados da pesquisa original do projeto SOFIA, conduzida na Universidade de Brasília (UnB) com financiamento do Ministério da Saúde. A atribuição ao trabalho original é mantida em respeito à sua fundação acadêmica.