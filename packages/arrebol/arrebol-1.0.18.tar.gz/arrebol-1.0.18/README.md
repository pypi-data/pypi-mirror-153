# Arrebol

<br>

Pacote criado com a finalidade única de testar como subir um pacote para o PyPi e Conda.

- https://github.com/traquitanas/arrebol
- https://anaconda.org/michelmetran/arrebol
- https://pypi.org/project/arrebol/

<br>

---

### _Build Manually_

Inicialmente é necessário instalar o [conda-build](https://docs.conda.io/projects/conda-build/en/latest/index.html) com o comando:

```bash
conda activate pablocarreira-py39
conda install conda-build
```

<br>

Uma vez instalado, é possível buildar com o comando abaixo:

```bash
conda-build ./conda/
```

<br>

---

### GitActions

Há um [GitAction](https://github.com/fcakyon/conda-publish-action) para publicar pacotes no Conda. A vantagem é que ele converte o _build_ para outras plataformas (adicionar converters)!

Já tentei outros, porém abandonei por falhas:

- elbeejay/conda-publish-action@v1.5
- maxibor/conda-package-publish-action@v1.1

<br>

```bash
# Convert Package to Other Platforms
cd ~
platforms=( osx-64 linux-32 linux-64 win-32 win-64 )
find $HOME/conda-bld/linux-64/ -name *.tar.bz2 | while read file
do
    echo $file
    #conda convert --platform all $file  -o $HOME/conda-bld/
    for platform in "${platforms[@]}"
    do
       conda convert --platform $platform $file  -o $HOME/conda-bld/
    done
done
```

<br>

---

### Referências

- [Conda-Build: Conda channels](https://docs.conda.io/projects/conda-build/en/latest/concepts/channels.html)
- [Medium: Publishing Your Python Package on conda and conda-forge](https://levelup.gitconnected.com/publishing-your-python-package-on-conda-and-conda-forge-309a405740cf)
- [YouTube: Building and Distributing Python Software with Conda](https://www.youtube.com/watch?v=HSK-6dCnYVQ)
- [Medium: Building a conda package and uploading it to Anaconda Cloud](https://giswqs.medium.com/building-a-conda-package-and-uploading-it-to-anaconda-cloud-6a3abd1c5c52) Não gostei pois é preciso etapas manuais

**GitActions**

- https://github.com/maxibor/conda-package-publish-action
- https://github.com/rfun/tethysapp-servicetest/blob/master/.github/workflows/main.yml
