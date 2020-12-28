# Reinforcement learning - Risk

## Descrição

Programa para ensinar o computador a jogar o jogo de tabuleiro *Risk* por meio
de aprendizagem baseada em reforço. Trabalho final da disciplina Fundamentos
de sistemas inteligentes 2019/1 da Universidade de Brasília.

## Integrantes

Nome                           | Matrícula
-----------------------------  | ----------
André Filipe Caldas Laranjeira | 16/0023777
Victor André Gris Costa        | 16/0019311

## Implementação

A implementação utilizada para as regras do jogo *Risk* é uma adaptação das regras
encontradas no repositório [*pyrisk*](https://github.com/chronitis/pyrisk), feito
pelo usuário @chronitis. Como base nas classes do *pyrisk*, fizemos classes
novas com a mesma lógica do jogo mas que fossem mais facilmente integráveis
em uma classe `Env` da biblioteca *OpenAI gym*.
