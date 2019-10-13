
# Projeto1-Megadados

- Modelo Entidade-Relacionamento:

![MER](image%20(5).png)

- Modelo Relacional:

    - Schema/Diagrama do modelo relacional:
![tabelas](tabelas.PNG)
    - Dicionário de dados:
        - Tabela **usuarios**: Representa os atributos de cada um dos usuários
        
            | Nome do campo  | Descrição | Auto-gerada | Chave primária | Chave estrangeira | Referencia | Restrições |
            | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- |
            | ID_USUARIO  | id do usuário  | sim, auto-incrementa | sim | não | - | não nulo |
            | NOME  | nome do usuário  | não | não | não | - | não nulo |
            | EMAIL  | email do usuário  | não | não | não | - | não nulo |
            | CIDADE  | cidade onde mora o usuário  | não | não | não | - | não nulo |

            
        - Tabela **passaros**: Representa os atributos de cada um dos pássaros
        
            | Nome do campo  | Descrição | Auto-gerada | Chave primária | Chave estrangeira | Referencia | Restrições |
            | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- |
            | ID_PASSARO  | id do pássaro  | sim, auto-incrementa | sim | não | - | não nulo |
            | PASSARO  | nome do pássaro  | não | não | não | - | não nulo |
            
            
        - Tabela **post**: Representa os atributos de cada um dos posts
        
            | Nome do campo  | Descrição | Auto-gerada | Chave primária | Chave estrangeira | Referencia | Restrições |
            | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- |
            | ID_POST  | id do post  | sim, auto-incrementa | sim | não | - | não nulo |
            | TITULO  | título do post  | não | não | não | - | não nulo |
            | URL  | URL de uma foto do post  | não | não | não | - | - |
            | TEXTO  | texto escrito no post  | não | não | não | - | - |
            | ID_CRIADOR  | id do criador do post  | não | não | sim | ID_USUARIO da tabela usuário | não nulo |
            | ATIVO  | se o post está ativo ou não  | sim, padrão 1 | não | não | - | não nulo |
            | DATA_CRIACAO  | quando foi criado o post  | sim, timestamp | não | não | - | não nulo |


        - Tabela **preferencias**: Representa quais pássaros cada usuário prefere
        
            | Nome do campo  | Descrição | Auto-gerada | Chave primária | Chave estrangeira | Referencia | Restrições |
            | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- |
            | ID_PASSARO  | id do pássaro  | não | não | sim | ID_PASSARO da tabela pássaro | não nulo |
            | ID_USUARIO  | id do usuário  | não | não | sim | ID_USUARIO da tabela usuário | não nulo |
            
        - Tabela **mark_user_post**: Representa quais usuários foram marcados em cada post
        
            | Nome do campo  | Descrição | Auto-gerada | Chave primária | Chave estrangeira | Referencia | Restrições |
            | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- |
            | ID_POST  | id do post  | não | não | sim | ID_POST da tabela post | não nulo |
            | ID_USUARIO  | id do usuário  | não | não | sim | ID_USUARIO da tabela usuário | não nulo |
            | ATIVO  | se o post está ativo ou não  | sim, padrão 1 | não | não | - | não nulo |
            
        - Tabela **post_passaro**: Representa quais pássaros foram marcados em cada post
        
            | Nome do campo  | Descrição | Auto-gerada | Chave primária | Chave estrangeira | Referencia | Restrições |
            | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- |
            | ID_POST  | id do post  | não | não | sim | ID_POST da tabela post | não nulo |
            | ID_PASSARO  | id do pássaro  | não | não | sim | ID_PASSARO da tabela pássaro | não nulo |
            | ATIVO  | se o post está ativo ou não  | sim, padrão 1 | não | não | - | não nulo |
            
        - Tabela **view_user_post**: Representa quais pássaros cada usuário prefere
        
            | Nome do campo  | Descrição | Auto-gerada | Chave primária | Chave estrangeira | Referencia | Restrições |
            | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- |
            | ID_POST  | id do post  | não | não | sim | ID_POST da tabela post | não nulo |
            | ID_USUARIO  | id do usuário  | não | não | sim | ID_USUARIO da tabela usuário | não nulo |
            | BROWSER  | em qual navegador o usuário visualizou o post  | não | não | não | - | - |
            | APARELHO  | em qual aparelho o usuário visualizou o post  | não | não | não | - | - |
            | IP  | ip do aparelho no qual o usuário visualizou o post  | não | não | não | - | - |
            | INSTANTE_VISUALIZACAO  | momento em que o usuário visualizou o post | sim, timestamp | não | não | - | não nulo |
            | ATIVO  | se o post está ativo ou não  | não | sim, padrão 1 | não | - | não nulo |

