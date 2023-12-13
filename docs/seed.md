# Seed

Em `scripts/seed.py` são criados alguns dados para facilitar o desenvolvimento
e alguns testes manuais. Dados como universidade, unidades consumidoras, 
contratos e etc. Leia o script para entender como eles se relacionam.

Os comandos a seguir também devem ser executados dentro do container da api 
(mec-energia-api).
Note que esses comandos executam scripts em bash. Eles fazem pipe dos conteúdos
expressos `seed_UNB.py` e `seed_UFMG.py` para o shell do Django.


Para popular o banco com o **seed de demonstração** execute **dentro do container da API** o seguinte:

```sh
./scripts/seed_demo.sh
```

O seed de demonstração da entrega do projeto popula o banco com dados da UNB e da
UFMG.

Para apagar os dados do banco de dados você pode usar:

```sh
./scripts/dbflush.sh
```

**Execute o comando anterior com cuidado!**. Esse script pula o prompt de 
confirmação e apaga todos os dados diretamente.

## Usuários

Para acessar dados da API e a documentação, você deve criar um usuário. O script
`seed.py` já cria um _usuário de universidade_. Logar com esse usuário te dá a
perspectiva de um usuário de universidade. As credenciais desse usuário estão
em `seed.py`.

Além desse usuário, você pode criar um super usuário. Para isso basta rodar

```sh
./scripts/create-superuser.sh
```

A senha e o email estão `scripts/create-superuser.sh`. Você deve usá-los para
logar na API.
