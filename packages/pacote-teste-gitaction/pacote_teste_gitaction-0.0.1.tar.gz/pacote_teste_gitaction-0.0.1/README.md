# Build GitAction

<br>

Tester Git Actions: publicar pacotes no PyPi

Publicar versões de distribuição de pacotes usando fluxos de trabalho de CI / CD de ações do GitHub. Ver mais [aqui](https://packaging.python.org/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/).

**IMPORTANTE**: Adicionar as credenciais do PyPi, da versão test e versão estável, como um Secrets do GitHub, sob os nomes PYPI_API_TOKEN e TEST_PYPI_API_TOKEN.

<br>

**_Tags_**

Note que a função tem uma condição: o pacote só é publicado quando há uma tag de versão no _commit_. Isso condicionante pode ser suprimida ou empregada. É preciso entender os conceitos de [tags](https://git-scm.com/book/en/v2/Git-Basics-Tagging) em _commits_ e como fazer isso usando o [PyCharm](https://www.jetbrains.com/help/pycharm/use-tags-to-mark-specific-commits.html#tag_commit) ou outra IDE
