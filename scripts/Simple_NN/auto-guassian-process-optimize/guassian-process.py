#imports we know we'll need
import skopt
# !pip install scikit-optimize if  necessary
from skopt import gbrt_minimize, gp_minimize
from skopt.utils import use_named_args
from skopt.space import Real, Categorical, Integer  
from generate_yaml import create_yaml_file
from submit_qsub import submit_simple_nn_job_and_wait_sync

import pickle

dim_learning_rate = Real(low=1e-4, high=1e-2, prior='log-uniform',
                            name='learning_rate')
dim_num_layer_1 = Integer(low=1, high=1000, name='layer_1')
dim_num_layer_2 = Integer(low=1, high=1000, name='layer_2')
dim_num_layer_3 = Integer(low=1, high=1000, name='layer_3')
dim_num_layer_4 = Integer(low=1, high=1000, name='layer_4')
dim_num_layer_5 = Integer(low=1, high=1000, name='layer_5')
dim_num_layer_6 = Integer(low=1, high=1000, name='layer_6')
dim_num_layer_7 = Integer(low=1, high=1000, name='layer_7')
dim_activation = Categorical(categories=['relu', 'sigmoid', 'tanh'],
                            name='activation')
dim_batch_size = Integer(low=1, high=500, name='batch_size')

dimensions = [dim_learning_rate,
            dim_num_layer_1,
            dim_num_layer_2,
            dim_num_layer_3,
            dim_num_layer_4,
            dim_num_layer_5,
            dim_num_layer_6,
            dim_num_layer_7,
            dim_activation,
            dim_batch_size
            ]

def create_guassian_process():
    default_parameters = [1e-3, 200,200,200,200,200,200,200, 'relu', 64]
    gp_result = gp_minimize(func=fitness,
                            dimensions=dimensions,
                            n_calls=12,
                            noise= 0.01,
                            n_jobs=-1,
                            kappa = 5,
                            x0=default_parameters)
    results_file = open("df_gp_res.pickle","wb")
    pickle.dump(gp_result, results_file)

@use_named_args(dimensions=dimensions)
def fitness(learning_rate, layer_1, layer_2, layer_3, layer_4, layer_5, layer_6, layer_7,
            activation, batch_size):
    yaml = create_yaml_file(learning_rate, layer_1, layer_2, layer_3, layer_4, layer_5, layer_6, layer_7,activation,batch_size)
    val_returned = submit_simple_nn_job_and_wait_sync(yaml)
    return val_returned*100

create_guassian_process()