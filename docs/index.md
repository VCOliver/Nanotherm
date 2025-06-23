# **Bem-vindo à Documentação do Nanotherm**

O Nanotherm é uma plataforma moderna para ablação por radiofrequência (RFA) desenvolvida pela Metala Nanofluidos, baseada no projeto [SOFIA](https://noticias.unb.br/117-pesquisa/2018-prototipo-desenvolvido-na-unb-ganha-premio-de-inovacao). Esta documentação detalha como instalar, configurar e usar o sistema.

## Instalação

O Nanotherm requer Python 3.12 ou superior. Recomendamos usar o Conda para gerenciar o ambiente:

```bash
# Clone o repositório
git clone https://github.com/VCOliver/Nanotherm
cd Nanotherm

# Crie e ative o ambiente conda
conda env create -f environment.yml
conda activate nanotherm-venv

# Instale o pacote em modo de desenvolvimento
poetry install
```

## Configuração

O sistema usa um arquivo TOML para configuração. Um exemplo básico:

```toml
[logging]
level = "DEBUG"  # Ou "deploy" para produção
format = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
date_format = "%d-%m-%Y %H:%M:%S"

[pid]
kp = 1.0
ki = 0.2
kd = 0.05
```

## Uso Básico

Para executar o Nanotherm:

```bash
# Via poetry
poetry run nanotherm

# Ou diretamente após instalação
python -m nanotherm
```

## Estrutura do Projeto

```
 src/nanotherm/           # Código fonte principal
    ├── app/                # Aplicação principal e entry points
    ├── core/              # Core business logic
    │   ├── domain/       # Domain models and value objects
    │   └── entities/     # Core business interfaces
    ├── infrastructure/   # Concrete implementations
    │   └── controllers/  # Controller implementations
    ├── services/        # Application services
    └── config/         # Configuration management
```

O projeto segue uma arquitetura limpa (Clean Architecture) com separação clara entre:
- **Domain**: Regras de negócio e interfaces core
- **Infrastructure**: Implementações concretas
- **Services**: Orquestração de componentes

## Licença

O Nanotherm é licenciado sob Apache License 2.0. Veja o arquivo LICENSE para mais detalhes.

## Links Úteis

- [Código fonte](https://github.com/VCOliver/Nanotherm)
- [Documentação da API](reference/main.md)
- [Sobre o projeto](about.md)

## Suporte

Para suporte ou dúvidas, entre em contato:
- Email: metala.nanofluidos@gmail.com
- Site: [metalanano.com](https://metalanano.com)

