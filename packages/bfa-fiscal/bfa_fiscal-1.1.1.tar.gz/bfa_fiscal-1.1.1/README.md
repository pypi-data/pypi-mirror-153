# bfa-fiscal

## Instrucciones de instalación

1) Comentar la línea 362 del archivo /etc/ssl/openssl.cnf donde dice:
```
CipherString = DEFAULT@SECLEVEL=2
```

2) Instalar python3-m2crypto, pip3:

```
# echo "deb http://deb.debian.org/debian buster-backports main" >> /etc/apt/sources.list

# apt update

# apt install python3-m2crypto python3-pip python3-httplib2
```

*Opcional*: Desisntalar python3-pysimplesoap

```
# apt purge -y python3-pysimplesoap && apt autoremove -y
```

3) Instalar **bfa-fiscal**:
```
# pip3 install bfafiscal
```