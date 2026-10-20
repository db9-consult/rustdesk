# RustDesk DB9 1.5.0 — Android ARM64

Baixe `rustdesk-db9-1.5.0-aarch64.apk` em um dispositivo Android ARM64 (arm64-v8a).

1. Abra o APK e, se solicitado, permita que o navegador ou gerenciador de arquivos instale este aplicativo. Essa autorização pode ser removida após a instalação.
2. Abra **RustDesk DB9**. O servidor ID e relay `rustdesk.db9consult.com.br` e a chave pública DB9 já estão incorporados. Configurações salvas pelo usuário têm precedência e continuam editáveis.
3. Cadastre no Conta Única o número de **Seu ID** e solicite atendimento.
4. Inicie o compartilhamento de tela no aplicativo e confirme a permissão de captura do Android. Autorize a conexão do atendente quando solicitada. Para controle por toque, conceda a permissão de Acessibilidade ao **RustDesk DB9** quando necessário; ela pode exigir liberação de configurações restritas nas informações do aplicativo.

O pacote `com.db9consult.rustdesk` pode coexistir com o RustDesk oficial. As configurações do aplicativo oficial não são migradas. Atualizações DB9 usam a mesma assinatura permanente e são instaladas manualmente por APK.

`ANDROID-SHA256SUMS.txt` contém os checksums; `android-build-metadata.json` identifica as fontes, o certificado e a execução de compilação. `rustdesk-db9-1.5.0-android-source.tar.gz` inclui as fontes correspondentes e o submódulo hbb_common, preservando licenças e atribuições. A assinatura é própria da DB9 e não representa publicação na Google Play.

A validação automatizada verifica assinatura, arquitetura, metadados e presença da configuração incorporada. Uma sessão real de suporte requer validação em um dispositivo Android ARM64 autorizado.
