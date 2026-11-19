# Transferência — MEINERZ UNIFORM STUDIO

## Destino de continuidade

https://github.com/AtlasAndreiRaimundi/Meinerz-Uniform-Studio

Origem histórica: https://github.com/AtlasAndreiRaimundi/Atlas-Uniform-Studio

As 35 branches existentes foram copiadas sem reescrever commits. A main de
origem no início da cópia era `cc9d729a28c31a450b1d59633dd39c104faab156`.
O repositório original foi preservado.

## Fonte atual do Sites

Projeto: `appgprj_6ad921f302148191932d8c1e12374ce3`.

Versão 133, commit `586bc06e787d376b6670691a9ce955798dda6b14`.
O checkout autorizado retornou exatamente esse commit.
O arquivo `source-manifest.json` registra o commit efetivamente exportado e
os hashes SHA-256 por arquivo. Use o manifesto como evidência da exportação.

## Validação executada

- Exportação: 7.029 arquivos; 5.775.546.531 bytes antes da compactação Git.
- `python scripts/restore_source.py`: 7.029 hashes SHA-256 conferidos.
- `python scripts/check_source.py`: varredura de padrões de segredos aprovada.
- `node --test tests/*.test.mjs`: 768 testes, 354 aprovados, 403 falharam,
  11 ignorados. O ambiente não tem as dependências instaladas; apareceram
  módulos ausentes como exceljs, pdf-lib, jszip e vite, além de casos do
  simulador rejeitados pela validação de modelagem. Isso não equivale a uma
  homologação funcional da versão 133. Não foram corrigidos testes ou código
  funcional durante a cópia; os bytes da fonte exportada foram preservados.
- Build, typecheck e conferência visual não executados nesta transferência.

Na nova conta, instalar as dependências conforme o projeto e repetir a suíte,
typecheck e build antes de desenvolver ou publicar. A entrega comprova a
integridade da cópia, não ausência de defeitos na aplicação.

## Limites da transferência Git

Não transfere banco, objetos de usuários, segredos, titularidade da hospedagem,
domínios ou autenticação. Não houve deploy nem migração de dados nesta entrega.
Issues, pull requests, comentários e histórico de Actions continuam na origem;
as branches de trabalho correspondentes foram preservadas no destino.

Instruções para a nova conta: [CONTINUAR-NA-OUTRA-CONTA.md](CONTINUAR-NA-OUTRA-CONTA.md).
