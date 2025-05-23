#!/bin/bash

# Script para executar a aplicação Teste Tivit

set -e

echo "🚀 Teste Tivit API - Setup e Execução"
echo "======================================"

# Função para mostrar ajuda
show_help() {
    echo "Uso: ./run.sh [COMANDO]"
    echo ""
    echo "Comandos disponíveis:"
    echo "  setup     - Configurar ambiente de desenvolvimento"
    echo "  dev       - Executar em modo desenvolvimento"
    echo "  docker    - Executar com Docker Compose"
    echo "  test      - Executar testes"
    echo "  clean     - Limpar containers e volumes"
    echo "  help      - Mostrar esta ajuda"
    echo ""
}

# Função para setup do ambiente
setup_env() {
    echo "📦 Configurando ambiente..."
    
    # Criar ambiente virtual se não existir
    if [ ! -d "venv" ]; then
        echo "Criando ambiente virtual..."
        python3 -m venv venv
    fi
    
    # Ativar ambiente virtual
    echo "Ativando ambiente virtual..."
    source venv/bin/activate
    
    # Instalar dependências
    echo "Instalando dependências..."
    pip install --upgrade pip
    pip install -r requirements.txt
    
    echo "✅ Ambiente configurado com sucesso!"
}

# Função para executar em modo desenvolvimento
run_dev() {
    echo "🔧 Executando em modo desenvolvimento..."
    
    # Verificar se o ambiente virtual existe
    if [ ! -d "venv" ]; then
        echo "❌ Ambiente virtual não encontrado. Execute: ./run.sh setup"
        exit 1
    fi
    
    # Ativar ambiente virtual
    source venv/bin/activate
    
    # Executar aplicação
    echo "Iniciando servidor de desenvolvimento..."
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
}

# Função para executar com Docker
run_docker() {
    echo "🐳 Executando com Docker Compose..."
    
    # Parar containers existentes
    docker-compose down
    
    # Construir e executar
    docker-compose up --build
}

# Função para executar testes
run_tests() {
    echo "🧪 Executando testes..."
    
    # Verificar se o ambiente virtual existe
    if [ ! -d "venv" ]; then
        echo "❌ Ambiente virtual não encontrado. Execute: ./run.sh setup"
        exit 1
    fi
    
    # Ativar ambiente virtual
    source venv/bin/activate
    
    # Executar testes
    pytest -v
}

# Função para limpar containers
clean_docker() {
    echo "🧹 Limpando containers e volumes..."
    
    docker-compose down -v
    docker system prune -f
    
    echo "✅ Limpeza concluída!"
}

# Processar argumentos
case "${1:-help}" in
    setup)
        setup_env
        ;;
    dev)
        run_dev
        ;;
    docker)
        run_docker
        ;;
    test)
        run_tests
        ;;
    clean)
        clean_docker
        ;;
    help|*)
        show_help
        ;;
esac
