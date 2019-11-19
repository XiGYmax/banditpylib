```
 _                     _ _ _               _ _ _     
| |                   | (_) |             | (_) |    
| |__   __ _ _ __   __| |_| |_ _ __  _   _| |_| |__  
| '_ \ / _` | '_ \ / _` | | __| '_ \| | | | | | '_ \ 
| |_) | (_| | | | | (_| | | |_| |_) | |_| | | | |_) |
|_.__/ \__,_|_| |_|\__,_|_|\__| .__/ \__, |_|_|_.__/ 
                              | |     __/ |          
                              |_|    |___/                
```

A lightweight python library for bandit algorithms

## Features

* object-oriented
* multiprocesses support
* easy to debug

## Implemented Policies

### Regret Minimization

#### Ordinary Bandit

* Uniform
* Epsilon Greedy
* UCB [[1]](#ACF02)
* MOSS [[2]](#AB09)
* Thompson Sampling \[[3](#T33), [4](#KKM12)\]
* UCBV [[5]](#AMS09)

#### Ordinary MNL Bandit

* Exploration-exploitation [[6]](#AAGZ19)

### Best Arm Identification

#### Ordinary MNL Bandit

##### Fixed Budget 

* Uniform
* SR [[7]](#AB10)

## Running of the Project

### Quick Run

```shell
# install required packages under the vitual environment
# python 3 is used
python -m venv env
source env/bin/activate
pip install -r requirements.txt
# run under `banditpylib` directory
python main.py
deactivate
```

The output is put to `out/figure.pdf` by default and the output figure is like the following.

![output example](figures/example.jpg)

### Other Options

```shell
# run a simple setup for debug
python main.py --debug
# generate raw data
python main.py --do=d
# run all unit tests
python -m unittest discover
```

## TODO

* add figure output for best arm identification

## License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details.

## Acknowledgments

* This project is inspired by [libbandit](https://github.com/tor/libbandit) and [banditlib](https://github.com/jkomiyama/banditlib) which are both c++ libraries for bandit algorithms.
* This readme file is following the style of [README-Template.md](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2).
* The title is generated by [TAAG](http://patorjk.com/software/taag/#p=display&f=Graffiti&t=Type%20Something%20).

## References

1. <a name="ACF02"></a> Peter Auer, Nicolo Cesa-Bianchi, and Paul Fischer. Finite-time analysis of the multiarmed bandit problem. Machine learning, pages 235–256, 2002.
2. <a name="AB09"></a> Jean-Yves Audibert and Sébastien Bubeck. Minimax Policies for Adversarial and Stochastic Bandits. In COLT, 2009.
3. <a name="T33"></a> William R Thompson. On the likelihood that one unknown probability exceeds another in view of the evidence of two samples. Biometrika, 25(3/4):285–294, 1933.
4. <a name="KKM12"></a> Emilie Kaufmann, Nathaniel Korda, and Rémi Munos. Thompson sampling: An asymptotically optimal finite-time analysis. In ALT, pages 199–213, 2012.
5. <a name="AMS09"></a> Jean-Yves Audibert, Rémi Munos, and Csaba Szepesvári. Exploration-exploitation tradeoff using variance estimates in multi-armed bandits. Theoretical Computer Science, 410(19):1876–1902, 2009.
6. <a name="AAGZ19"></a> Shipra Agrawal, Vashist Avadhanula, Vineet Goyal and Assaf Zeevi. MNL-bandit: A dynamic learning approach to assortment selection. Operation Research, 67(5):1453-1485, 2019.
7. <a name="AB10"></a> Jean-Yves Audibert and Sébastien Bubeck. Best arm identification in multi-armed bandits. In COLT, 2010.
