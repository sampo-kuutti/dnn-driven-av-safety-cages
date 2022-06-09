# Safe deep neural network-driven autonomous vehicles using software safety cages

This is the repo for paper Safe deep neural network-driven autonomous vehicles using software safety cages. 
Train an imitation learning policy to control an autonomous agent for vehicle following. 
Additionally, safety cages can be used to ensure safety and provide additional training signal when the policy
makes a mistake.


## Installation
Clone the repo

```bash
git clone https://github.com/sampo-kuutti/dnn-driven-av-safety-cages
```

install requirements:
```bash
pip install -r requirements.txt
```

## Training the policy


To run the the training run `train_sl.py`.

## Citing the Repo

If you find the code useful in your research or wish to cite it, please use the following BibTeX entry.

```text
@inproceedings{kuutti2019safe,
  title={Safe deep neural network-driven autonomous vehicles using software safety cages},
  author={Kuutti, Sampo and Bowden, Richard and Joshi, Harita and de Temple, Robert and Fallah, Saber},
  booktitle={International Conference on Intelligent Data Engineering and Automated Learning},
  pages={150--160},
  year={2019},
  organization={Springer, Cham}
}
```
