YAML_TEMPLATE_1 = """
generate_features: true
preprocess: true
train_model: true
atom_types:
 - H
 - O

symmetry_function:
  params:
    H: params_H
    O: params_O
       
neural_network:
  use_force: true
  method: Adam
  force_coeff: 1
  nodes: {}-{}-{}-{}-{}-{}-{}
  full_batch: false
  activation_function: {}
  batch_size: {}
  total_epoch: 10000
  learning_rate: {}
"""

YAML_TEMPLATE_2 = """
generate_features: true
preprocess: true
train_model: true
atom_types:
 - H
 - O

symmetry_function:
  params:
    H: params_H
    O: params_O
       
neural_network:
  use_force: true
  method: Adam
  force_coeff: 1
  nodes: {}
  full_batch: false
  activation_function: {}
  batch_size: {}
  total_epoch: 10000
  learning_rate: {}
"""

def create_yaml_file(dim_learning_rate, dim_num_layer_1, dim_num_layer_2, dim_num_layer_3, dim_num_layer_4,
              dim_num_layer_5, dim_num_layer_6, dim_num_layer_7, dim_activation,
              dim_batch_size):
    return YAML_TEMPLATE_1.format(dim_num_layer_1,dim_num_layer_2,dim_num_layer_3,dim_num_layer_4,dim_num_layer_5,dim_num_layer_6,dim_num_layer_7,dim_activation,dim_batch_size,dim_learning_rate)

def create_yaml_file_variable_layers(dim_learning_rate, dim_layer_size, dim_layers, dim_activation, dim_batch_size):
    nodes_string = "-".join(str(x) for x in ([dim_layer_size] * dim_layers))
    return YAML_TEMPLATE_2.format(nodes_string, dim_activation, dim_batch_size, dim_learning_rate)

def create_yaml_file_layer_encoding(learning_rate, layers, size, shape, growth,
            activation, batch_size):
    if(shape == "block"):
        nodes_string = "-".join(str(x) for x in ([size] * layers))
        return YAML_TEMPLATE_2.format(nodes_string, activation, batch_size, learning_rate)
    if(shape == "diamond"):
        nodes = []
        if(layers % 2 == 1):
            layer_size = size
            for layer in range(layers//2):
                nodes.append(layer_size)
                layer_size = layer_size + growth
            reverse_list = nodes[::-1]
            nodes.append(layer_size)
            nodes = nodes + reverse_list
        else:
            layer_size = size
            for layer in range(layers//2):
                nodes.append(layer_size)
                layer_size = layer_size + growth
            reverse_list = nodes[::-1]
            nodes = nodes + reverse_list
        nodes_string = "-".join(str(x) for x in nodes)
        return YAML_TEMPLATE_2.format(nodes_string, activation, batch_size, learning_rate)
    if(shape == "bowtie"):
        nodes = []
        if(layers % 2 == 1):
            layer_size = size
            for layer in range(layers//2):
                nodes.append(layer_size)
                layer_size = layer_size - growth
                if(layer_size < growth):
                    layer_size = growth
            reverse_list = nodes[::-1]
            nodes.append(layer_size)
            nodes = nodes + reverse_list
        else:
            layer_size = size
            for layer in range(layers//2):
                nodes.append(layer_size)
                layer_size = layer_size - growth
                if(layer_size < growth):
                    layer_size = growth
            reverse_list = nodes[::-1]
            nodes = nodes + reverse_list
        nodes_string = "-".join(str(x) for x in nodes)
        return YAML_TEMPLATE_2.format(nodes_string, activation, batch_size, learning_rate)