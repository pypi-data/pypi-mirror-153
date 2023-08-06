
# nyto

nyto是一款輕量化的python庫，方便使用者快速開發元啟發算法(metaheuristic)訓練內建的深度學習模型。

## 說明

基於梯度下降的深度學習工具可以幫助我們快速建立並訓練深度學習模型，然而在有些情況下基於梯度下降的訓練方式可能會遇到問題，這時後我們可以借助其他優化方式來達成目的。

本庫提供了一個界面，方便使用者編寫自己的元啟發算法來優化網路。而倘若你對編寫算法沒有興趣，本庫也已經內建了一個基於粒子群算法(Particle swarm optimization)的算法可供使用。

詳細介紹可以查看[Introduction_of_nyto](https://github.com/jimmyzzzz/Introduction_of_nyto)，該頁面提供了使用介紹和範例程式。

## 快速入門

### 安裝

安裝nyto需要預先安裝python3.6或更高的版本，以及pip和numpy。而通常pip會與python一起安裝。

從PyPI安裝:
```bash
$ pip install nyto
```

### 快速建立網路

在nyto中建立網路分成兩步驟:
1. 導入模型: 可以想成是建立網路所需的零件
2. 連接節點: 可以想成是將零件組成網路

```python
from nyto import net_tool as to
from nyto import layer
from nyto import unit_function as uf

# 導入模型
my_net, node = to.new_net()
node.layer1 = layer.new_nn_layer((4,12))
node.layer2 = layer.new_nn_layer((12,3))

# 連接節點
node.layer1_output = node.layer1_input >> node.layer1 >> uf.tanh()
node.layer2_output = node.layer1_output >> node.layer2 >> uf.softmax()
```
### 粒子運算

在nyto中，網路都是視為粒子群演算法中的粒子，當對網路做`+1`的操作時，網路中的所有參數都會+1。而當我們將多個網路進行粒子運算時，則可以實現元啟發算法中所有優化所需的一切功能。

**網路與數值運算**

當對網路本身進行運算時，可以視為對粒子的移動:
```python
new_net = my_net + 1
```
<img src="https://imgur.com/qQP5w8x.png" width="60%" height="60%">

**網路間運算**

當網路對網路進行運算時，可以視為對粒子進行組合:
```python
new_net = my_net + other_net
```
<img src="https://imgur.com/lQOGVLv.png" width="60%" height="60%">

### 取得某些節點的輸出值

當想要查看特定網路中節點的輸出結果時可以使用`net_tool.get`來查看:
```python
from nyto.net_tool import get

layer1_return,layer2_return = get(node.layer1_output, node.layer2_output)
```