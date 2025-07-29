#!/bin/bash

# Cria diretório para as chaves DKIM
mkdir -p dkim_keys
cd dkim_keys

# Gera chave privada
openssl genrsa -out private.key 2048

# Gera chave pública
openssl rsa -in private.key -pubout -out public.key

echo "Chaves DKIM geradas em dkim_keys/"
