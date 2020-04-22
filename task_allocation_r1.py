from pyomo.environ import *

N_worker = 3
N_task = 10

worker_cur_load = {1:1, 2:2, 3:12}

task_load = {1:1, 2:2, 3:3, 4:4, 5:1, 6:2, 7:4, 8:5, 9:2, 10:2}

task_type = {1:1, 2:2, 3:3, 4:2, 5:2, 6:3, 7:1, 8:2, 9:3, 10:1}

#competence worker,task_type
competence = {(1, 1): 1, (1, 2): 1, (1, 3): 0,
				(2, 1): 1, (2, 2): 0, (2, 3): 1,
				(3, 1): 0, (3, 2): 1, (3, 3): 1}

model = ConcreteModel()

model.workers = range(1,N_worker+1)
model.tasks = range(1,N_task+1)

model.z = Var( within=PositiveIntegers )

model.x = Var( model.workers, model.tasks, within=Binary )

model.obj = Objective(expr=model.z, sense=minimize)

model.aux_z = ConstraintList()

for n in model.workers:
	model.aux_z.add(model.z >= worker_cur_load[n] + \
	sum(model.x[n,m]*task_load[m] for m in model.tasks))
	
model.single_x = ConstraintList()

for m in model.tasks:
	model.single_x.add( sum( model.x[n,m] for n in model.workers ) == 1.0 )
	
model.competence_req = ConstraintList()

for m in model.tasks:
	model.competence_req.add( sum( model.x[n,m]*competence[n,task_type[m]] for n in model.workers ) == 1.0 )
	