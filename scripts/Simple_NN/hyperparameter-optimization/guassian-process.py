#imports we know we'll need
import skopt
# !pip install scikit-optimize if  necessary
from skopt import gbrt_minimize, gp_minimize
from skopt.utils import use_named_args
from skopt.space import Real, Categorical, Integer  
from generate_yaml import create_yaml_file_layer_encoding
from submit_qsub import submit_simple_nn_job_and_wait_sync
from skopt import Optimizer
from joblib import Parallel, delayed


import pickle

dim_learning_rate = Real(low=1e-4, high=1e-2, prior='log-uniform',
                            name='learning_rate')
dim_num_layers = Integer(low=2, high=6, name='layers')
dim_layer_size = Integer(low=50, high=500, name='size')
dim_layer_shape = Categorical(categories=['block', 'diamond', 'bowtie'],
                            name='shape')
dim_layer_shape_growth = Integer(low=10, high=40, name="growth")
dim_activation = Categorical(categories=['relu', 'sigmoid', 'tanh'],
                            name='activation')
dim_batch_size = Integer(low=1, high=400, name='batch_size')

dimensions = [dim_learning_rate,
            dim_num_layers,
            dim_layer_size,
            dim_layer_shape,
            dim_layer_shape_growth,
            dim_activation,
            dim_batch_size
            ]

def create_guassian_process():
    default_parameters_1 = [1e-3, 3,200,"block",10, 'relu', 64]
    default_parameters_2 = [1e-3, 3,200,"bowtie",10, 'relu', 64]
    default_parameters_3 = [1e-3, 3,200,"diamond",10, 'relu', 64]
    x0 = []
    x0.append(default_parameters_1)
    x0.append(default_parameters_2)
    x0.append(default_parameters_3)
    optimizer = Optimizer(
        dimensions=dimensions,
        random_state=1,
        n_initial_points=3,
        base_estimator='gp'
        )
    y = Parallel(n_jobs=3)(delayed(fitness)(v) for v in x0)
    optimizer.tell(x0, y)
    for run in range(20):
        x = optimizer.ask(n_points=3)
        y = Parallel(n_jobs=3)(delayed(fitness)(v) for v in x)
        print(str(val) for val in y)
        optimizer.tell(x, y)
    # gp_result = gp_minimize(func=fitness,
    #                         dimensions=dimensions,
    #                         n_calls=12,
    #                         noise= 0.01,
    #                         n_jobs=-1,
    #                         kappa = 5,
    #                         x0=default_parameters)
    results_file = open("df_gp_res.pickle","wb")
    pickle.dump(optimizer, results_file)

@use_named_args(dimensions=dimensions)
def fitness(learning_rate, layers, size, shape, growth,
            activation, batch_size):
    yaml = create_yaml_file_layer_encoding(learning_rate, layers, size, shape, growth,
            activation, batch_size)
    val_returned = submit_simple_nn_job_and_wait_sync(yaml)
    return val_returned*100

create_guassian_process()