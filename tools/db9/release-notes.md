# RustDesk 1.5.0 — DB9 Consult

Cliente baseado na versão 1.5.0 do RustDesk com os padrões incorporados:

- Servidor ID: `rustdesk.db9consult.com.br`
- Servidor Relay: `rustdesk.db9consult.com.br`
- Chave: `dksPMYTN32cCIMoIhBsKh5MZzYIAYt70xQxIiYZqSiQ=`

Os campos permanecem editáveis. Configurações já salvas têm precedência sobre esses padrões. Renomear o executável não altera os valores incorporados.

## Instalação

- Windows 64 bits: execute o EXE para uso portátil ou instale o MSI como administrador. Para instalação silenciosa: `msiexec /i rustdesk-db9-1.5.0-x86_64.msi /qn`.
- macOS Intel: monte o DMG `x86_64` e arraste RustDesk.app para Aplicativos.
- macOS Apple Silicon: use o DMG `aarch64`. Esta compilação segue o mínimo macOS 12.3 do upstream para ARM64.
- No macOS, conceda as permissões de Gravação de Tela e Acessibilidade quando solicitadas.

Os pacotes Windows não possuem certificado comercial. Os aplicativos macOS têm assinatura ad hoc, sem Apple Developer ID e sem notarização. O sistema pode exigir aprovação nas configurações de segurança para abrir o aplicativo.

Atualizações oficiais automáticas estão desativadas. Instale futuras versões manualmente pelas releases de https://github.com/db9-consult/rustdesk.

## Validação e fontes

Consulte os arquivos `db9-*-validation*.txt` e `db9-windows-tests.txt` para os testes realizados. Uma sessão interativa de controle remoto por relay entre dois dispositivos autorizados ainda requer validação operacional; a compilação não altera o servidor nem concede acesso automático.

`build-metadata.json` identifica o commit exato e o submódulo usados. `SHA256SUMS.txt` contém os checksums. O arquivo `rustdesk-db9-1.5.0-source.tar.gz` inclui o código correspondente e o submódulo hbb_common. A licença e as atribuições do RustDesk são preservadas.

## Superfície de regressão

- `src/lib.rs`: registro do módulo DB9.
- `src/common.rs`: inicialização dos padrões na GUI e nos serviços, e bloqueio da consulta ao serviço oficial de atualização.
- Novo módulo `src/db9.rs`: padrões editáveis dos três campos e política fixa de atualização manual.
- Novos workflows DB9: compilação e empacotamento derivados dos workflows da versão 1.5.0. Os workflows upstream e as revisões dos submódulos permanecem preservados.
