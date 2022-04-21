#!/usr/bin/env python3
###################BIBLIOTECAS######################################################
import os
import getpass
import sys
import argparse
import signal
import subprocess
import time 
from dataclasses import dataclass
from datetime import datetime
from multiprocessing import Process, Queue
from random import choice
import rospy
from actionlib_msgs.msg import GoalStatusArray
from gazebo_msgs.srv import SpawnModel
from gazebo_msgs.srv import DeleteModel
from geometry_msgs.msg import Pose
from geometry_msgs.msg import Point
from geometry_msgs.msg import Quaternion
from std_msgs.msg import Float64MultiArray
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal, MoveBaseActionResult
import actionlib
import analise 
import shutil

################PROCESSO DE SPAWN E GOALS ##########################################
def spawn_and_goals(q,q2,type,n,DATA_HORA):

    @dataclass
    class Ponto:
        x: float
        y: float
        w: float 

    

    def spawn_objects(obj,rota,name):
        try:
            if (rota == rota_AB) or (rota == rota_BC):
                try: 
                    a = choice(vetor1x)
                    b = choice(vetor1y)
                except: pass
                
                try: 
                    vetor1x.remove(a)
                    #vetor1y.remove(b)
                except: 
                    pass
            
                if (a == 4.3) or (a == 4.6) or (a == 5):
                    try: 
                        vetor1x.remove(4.3)
                    except: 
                        pass
                    try: 
                        vetor1x.remove(4.6)
                    except: 
                        pass
                    try: 
                        vetor1x.remove(5)
                    except: 
                        pass
            
                spawn_model_client(
                model_name=name,
                model_xml=open(os.path.expanduser('~')+"/modelo/"+obj+"/model.sdf",'r').read(),
                initial_pose = Pose(position= Point(a,b,0),orientation=Quaternion(0,0,0,2))
                )
            

            elif (rota == rota_CH) or (rota == rota_EC):
                a = choice(vetor2x)
                b = choice(vetor2y)
                try: 
                    #vetor2x.remove(a)
                    vetor2y.remove(b)
                except: 
                    pass
                if (b == 0.5) or (b == 0) or (b == -0.5):
                    try: 
                        vetor2y.remove(0.5)
                    except: 
                        pass
                    try: vetor2y.remove(0.0)
                    except: 
                        pass
                    try: 
                        vetor2y.remove(-0.5)
                    except: 
                        pass
                if (b == -13) or (b == -12.5) or (b == -12.0):
                    try: 
                        vetor2y.remove(-13)
                    except: 
                        pass
                    try: 
                        vetor2y.remove(-12.5)
                    except: 
                        pass
                    try: 
                        vetor2y.remove(-12.0)
                    except: 
                        pass
                if (b == -7.5) or (b == -8.5) or (b == -8.0):
                    try: 
                        vetor2y.remove(-8.5)
                    except: 
                        pass
                    try: 
                        vetor2y.remove(-7.5)
                    except: 
                        pass
                    try: 
                        vetor2y.remove(-8.0)
                    except: 
                        pass
                spawn_model_client(
                model_name=name,
                model_xml=open(os.path.expanduser('~')+"/modelo/"+obj+"/model.sdf",'r').read(),
                initial_pose = Pose(position= Point(a,b,0),orientation=Quaternion(0,0,0,2))
            )
        except: 
            a = -999
            b = -999
            rota = -999
        
        return a,b,rota

    def clear_objects():
        global vetor1x
        global vetor1y
        global vetor2x
        global vetor2y
        global array
        n_obstacles = 0
        while n_obstacles < args.o:
            try: 
                delete_model_client(
                    model_name = str(n_obstacles)
                 )
                n_obstacles += 1
                ###############Pode ser lançado em sombras###########################
                if args.ss == "true":
                    vetor1x = [-8,-7.5,-7,-6.5,-6,-4,-3.5,-3,-2.5,-2,0,0.5,1,1.5,2,4.3,4.6,5]
                    vetor1y = [-10.5,-11, -11.3]
                    vetor2y = [-13,-12.5,-12,-8.5,-8,-7.5,-5,-4.5,-4,-3.5,-3,-0.5,0,0.5,2,2.5,3,3.5,4,6,6.5,7,7.5,8]
                    vetor2x = [5.5,6.0,6.5]
                ###############Sempre em área da wsn###########################
                else:
                    vetor1x = [4.3,4.6,5]
                    vetor1y = [-10.5,-11, -11.3]
                    vetor2x = [5.5,6,6.5]
                    vetor2y = [-13,-12.5,-12,0,-0.5,0.5,-7.5,-8,-8.5]
                ######################################################################
                nothing = -999
                array = [nothing]*8
            except: pass
        
        pass

    def publish_wsn(pa, pb, rota):
        
        if (rota == rota_AB) or (rota == rota_BC): 
            if (pa >= 4):
                array[0] = float(pa)
                array[1] = float(pb)
                sensors = Float64MultiArray(data=array)
                wsn.publish(sensors)
        elif (rota == rota_CH) or (rota == rota_EC):
            if (pb >= -0.5) and (pb <= 0.5):
                array[6] = float(pa)
                array[7] = float(pb)
                sensors = Float64MultiArray(data=array)
                sensors = Float64MultiArray(data=array)
                wsn.publish(sensors)
            elif (pb <= -7.5) and (pb >= -8.5):
                array[4] = float(pa)
                array[5] = float(pb)
                sensors = Float64MultiArray(data=array)
                wsn.publish(sensors)
            elif (pb >= -13.0) and (pb <= -12.0):
                array[2] = float(pa)
                array[3] = float(pb)
                sensors = Float64MultiArray(data=array)
                wsn.publish(sensors)
        pass

    def set_goal(goal,pos):
        goal.target_pose.header.frame_id = 'map' 
        goal.target_pose.pose.position.x = pos.x
        goal.target_pose.pose.position.y = pos.y
        goal.target_pose.pose.orientation.z = 0.99
        goal.target_pose.pose.orientation.w = pos.w
        pass


    def spawn_and_goals_node(DATA_HORA):
        start_time = [0] * 8
        finish_time = [0] * 8
        diff_time = [0] * 8
        a = Ponto(6.5,-15,0)
        b = Ponto(-8.2,-11,0)
        c = Ponto(2.5,-11,0)
        d = Ponto(8,2.5,0)
        e = Ponto(4.5,2.5,0)
        f = Ponto(4.5,-2.5,0)
        g = Ponto(8,-2,0)
        h = Ponto(6.5,8,0)

        rospy.init_node('spawn_node')

        client = actionlib.SimpleActionClient('move_base',MoveBaseAction)

        goal = MoveBaseGoal()
        
        username = getpass.getuser()

        set_goal(goal,b)

        rospy.sleep(5)

        n_obstacles = 0
        while n_obstacles < args.o:
            pa, pb, rota = spawn_objects(person,rota_AB,str(n_obstacles))
            if (type == "full") and (rota != -999): publish_wsn(pa, pb, rota)
            if pa != -999: n_obstacles += 1
        
        print('Passed obstacles')
        top = subprocess.Popen(['cd ~/Análise_Simulações/'+DATA_HORA+'/Rota_AB; top -w 90 -i -d 2 -b -u ' + username + ' >> ' 
                                    + type], shell=True,preexec_fn=os.setpgrp)
        print('Passed TOP')
        client.send_goal(goal)
        start_time[1] = time.perf_counter()
        q.get()
        finish_time[1] = time.perf_counter()
        os.killpg(os.getpgid(top.pid), signal.SIGTERM)
        clear_objects()
        sensors = Float64MultiArray(data=array)
        wsn.publish(sensors)
        rospy.sleep(2)

        set_goal(goal,c)
        top = subprocess.Popen(['cd ~/Análise_Simulações/'+DATA_HORA+'/Rota_BC ; top -w 90 -i -d 2 -b -u ' + username + ' >> ' 
                                    + type], shell=True,preexec_fn=os.setpgrp)
        client.send_goal(goal)
        start_time[2] = time.perf_counter()
        rospy.sleep(0.5)

        if args.o != 1:
            n_obstacles = 0
            while n_obstacles < args.o:
                pa,pb,rota = spawn_objects(person,rota_BC,str(n_obstacles))
                if (type == "full") and (rota != -999): publish_wsn(pa, pb, rota)
                if pa != -999: n_obstacles += 1
        elif args.o == 1: pass
        q.get()
        finish_time[2] = time.perf_counter()
        os.killpg(os.getpgid(top.pid), signal.SIGTERM)
        clear_objects()
        sensors = Float64MultiArray(data=array)
        wsn.publish(sensors)
        rospy.sleep(2)

        set_goal(goal,h)
        top = subprocess.Popen(['cd ~/Análise_Simulações/'+DATA_HORA+'/Rota_CH ; top -w 90 -i -d 2 -b -u ' + username + ' >> ' 
                                    + type], shell=True,preexec_fn=os.setpgrp)
        client.send_goal(goal)
        start_time[3] = time.perf_counter()

        n_obstacles = 0
        while n_obstacles < args.o:
            pa,pb,rota = spawn_objects(person,rota_CH,str(n_obstacles))
            if (type == "full") and (rota != -999): publish_wsn(pa, pb, rota)
            if pa != -999: n_obstacles += 1

        q.get()
        finish_time[3] = time.perf_counter()
        os.killpg(os.getpgid(top.pid), signal.SIGTERM)
        clear_objects()
        sensors = Float64MultiArray(data=array)
        wsn.publish(sensors)
        rospy.sleep(2)

        set_goal(goal,d)
        top = subprocess.Popen(['cd ~/Análise_Simulações/'+DATA_HORA+'/Rota_HD ; top -w 90 -i -d 2 -b -u ' + username + ' >> ' 
                                    + type], shell=True,preexec_fn=os.setpgrp)
        client.send_goal(goal)
        start_time[4] = time.perf_counter()
        q.get()
        finish_time[4] = time.perf_counter()
        os.killpg(os.getpgid(top.pid), signal.SIGTERM)
        clear_objects()
        sensors = Float64MultiArray(data=array)
        wsn.publish(sensors)
        rospy.sleep(2)

        set_goal(goal,e)
        top = subprocess.Popen(['cd ~/Análise_Simulações/'+DATA_HORA+'/Rota_DE ; top -w 90 -i -d 2 -b -u ' + username + ' >> ' 
                                    + type], shell=True,preexec_fn=os.setpgrp)
        client.send_goal(goal)
        start_time[5] = time.perf_counter()
        q.get()
        finish_time[5] = time.perf_counter()
        os.killpg(os.getpgid(top.pid), signal.SIGTERM)
        clear_objects()
        sensors = Float64MultiArray(data=array)
        wsn.publish(sensors)
        rospy.sleep(2)

        set_goal(goal,c)
        top = subprocess.Popen(['cd ~/Análise_Simulações/'+DATA_HORA+'/Rota_EC ; top -w 90 -i -d 2 -b -u ' + username + ' >> ' 
                                    + type], shell=True,preexec_fn=os.setpgrp)
        client.send_goal(goal)
        start_time[6] = time.perf_counter()

        n_obstacles = 0
        while n_obstacles < args.o:
            pa,pb,rota = spawn_objects(person,rota_CH,str(n_obstacles)) 
            if (type == "full") and (rota != -999): publish_wsn(pa, pb, rota)
            if pa != -999: n_obstacles += 1
       
        q.get()
        finish_time[6] = time.perf_counter()
        os.killpg(os.getpgid(top.pid), signal.SIGTERM)
        clear_objects()
        sensors = Float64MultiArray(data=array)
        wsn.publish(sensors)
        rospy.sleep(2)
        
        set_goal(goal,a)
        top = subprocess.Popen(['cd ~/Análise_Simulações/'+DATA_HORA+'/Rota_CA ; top -w 90 -i -d 2 -b -u ' + username + ' >> ' 
                                    + type], shell=True,preexec_fn=os.setpgrp)
        client.send_goal(goal)
        start_time[7] = time.perf_counter()

        n_obstacles = 0
        while n_obstacles < args.o:
            pa,pb,rota = spawn_objects(person,rota_CH,str(n_obstacles))
            if (type == "full") and (rota != -999): publish_wsn(pa, pb, rota)
            if pa != -999: n_obstacles += 1


        q.get()
        finish_time[7] = time.perf_counter()
        os.killpg(os.getpgid(top.pid), signal.SIGTERM)
        clear_objects()
        sensors = Float64MultiArray(data=array)
        wsn.publish(sensors)
        rospy.sleep(2)

        q2.put([1])

        if type == "full": file = open(os.path.expanduser('~')+"/Análise_Simulações/"+DATA_HORA+"/time_file_full.txt", "a")
        elif type == "default": file = open(os.path.expanduser('~')+"/Análise_Simulações/"+DATA_HORA+"/time_file_default.txt", "a")
        file.write("-------------------------------------\n")
        file.write("-"+str(DATA_HORA)+"\n")

        for i in range(1,8,1):
            diff_time = finish_time[i] - start_time[i]
            file.write(str(i)+": "+str(round(diff_time,1))+"\n")

        file.close()    
        

        pass

    if __name__ == '__main__':
        try:
            trash_can = "first_2015_trash_can"
            person = "person_standing"
            rota_AB = 1
            rota_BC = 2
            rota_CH = 3 
            rota_HD = 4
            rota_DE = 5
            rota_EC = 6
            rota_CA = 7
            global vetor1x
            global vetor1y
            global vetor2x
            global vetor2y
            global array
            
            ###############Pode ser lançado em sombras###########################
            if args.ss == "true":
                vetor1x = [-8,-7.5,-7,-6.5,-6,-4,-3.5,-3,-2.5,-2,0,0.5,1,1.5,2,4.3,4.6,5]
                vetor1y = [-10.5,-11, -11.3]
                vetor2y = [-13,-12.5,-12,-8.5,-8,-7.5,-5,-4.5,-4,-3.5,-3,-0.5,0,0.5,2,2.5,3,3.5,4,6,6.5,7,7.5,8]
                vetor2x = [5.5,6.0,6.5]
            ###############Sempre em área da wsn###########################
            else:
                vetor1x = [4.3,4.6,5]
                vetor1y = [-10.5,-11, -11.3]
                vetor2x = [5.5,6,6.5]
                vetor2y = [-13,-12.5,-12,0,-0.5,0.5,-7.5,-8,-8.5]
            ######################################################################
            nothing = -999
            array = [nothing]*8
            rospy.init_node('spawn_node')
            spawn_model_client = rospy.ServiceProxy('/gazebo/spawn_sdf_model', SpawnModel)
            delete_model_client = rospy.ServiceProxy('/gazebo/delete_model', DeleteModel) 
            wsn = rospy.Publisher('wsn', Float64MultiArray, queue_size=10)
            time.sleep(1)
            spawn_and_goals_node(DATA_HORA)
            
        except rospy.ROSInterruptException: pass

###############PROCESSO PARA VERIFICAÇÃO DO FINAL DAS ROTAS#########################
def check_goal_reached(q):
    global aux
    aux = 0

    def goal_status(dado):
        global aux 
        try:
            if (dado.status_list[0].text == 'Goal reached.'):
                aux = aux + 1
                if aux == 1: 
                    q.put([1])
            else: 
                aux = 0 
        except:
            rospy.loginfo("No Goal Yet")
            pass

    def read_node():
        rospy.init_node('read_node')
        sub  = rospy.Subscriber("/move_base/status", GoalStatusArray, goal_status)
        pass

    try:
        time.sleep(2)
        read_node()
        rospy.spin()
            
    except rospy.ROSInterruptException: pass

##############FUNÇÃO LAUNCH DE SIMULAÇÃO ###########################################
def sim_laucher(tipo,rviz,gazebo,n, DATA_HORA):
    
    #if tipo == "full": flag_tipo_sim = 1 #flag_tipo_sim é utilizada para publicar os dados da wsn caso seja tipo full
    #elif tipo == "default": flag_tipo_sim = 0
    print(f'Simulation started: ', n, ' ', tipo)
    #top = subprocess.Popen(['cd ~/Análise_Simulações ; top -w 90 -i -d 1 -b -u pedro >> ' + DATA_HORA + '_'+tipo+'_'+str(n)], shell=True,preexec_fn=os.setpgrp)
    if tipo == "full": processo = subprocess.Popen(['roslaunch turtlebot3_gazebo turtlebot3_cedri_world_all.launch '+'rviz:='+str(rviz)
                                                        +' gazebo:='+str(gazebo)], shell=True, preexec_fn=os.setpgrp)
    
    elif tipo == "default": processo = subprocess.Popen(['roslaunch turtlebot3_gazebo turtlebot3_cedri_world_default.launch '+'rviz:='+str(rviz)
                                                        +' gazebo:='+str(gazebo)], shell=True, preexec_fn=os.setpgrp)                   
    q = Queue(maxsize=1)
    q2 = Queue(maxsize=1)
    time.sleep(5)
    check_process = Process(target=check_goal_reached, args=(q,))
    spawn_process = Process(target=spawn_and_goals, args=(q,q2,tipo,n,DATA_HORA))
    spawn_process.start()
    check_process.start()
    print('Processes created')
    q2.get()
    os.killpg(os.getpgid(processo.pid), signal.SIGTERM)
    #os.killpg(os.getpgid(top.pid), signal.SIGTERM)
    check_process.terminate()
    time.sleep(10)
    spawn_process.terminate()
    print(f'FINISHED', n, ' ', tipo)
    time.sleep(10)

    pass

###############FUNÇÃO PRINCIPAL#####################################################
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='arguments') 
    parser.add_argument('-t') #Tipo de setup full ou default ou both (Obrigatório)
    parser.add_argument('-n') #Número de rodadas (Obrigatório)
    parser.add_argument('-rv') #RVIZ true or false (Obrigatório)
    parser.add_argument('-gz') #Gazebo true or false (Obrigatório)
    parser.add_argument('-ss') #Sombras Spawn true or false (Default False)
    parser.add_argument('-o') #Número de obstáculos por rota (Default 1)
    parser.add_argument('-a') #Realiza análise após simulações true or false (Default False)
    args = parser.parse_args() 
    
    try: 
        path = os.path.expanduser('~')+"/Análise_Simulações"
        os.mkdir(path)
    except: pass
    
    n = 0
    DATA_HORA = str(datetime.today().strftime('%Y-%m-%d-%H:%M:%S'))
    path = os.path.expanduser('~')+"/Análise_Simulações/"+DATA_HORA
    os.mkdir(path)
    try: os.mkdir(path + '/Parâmetros_iniciais_TB3')
    except: pass
    rotas = ["Rota_AB", "Rota_BC", "Rota_CH", "Rota_HD", "Rota_DE", "Rota_EC", "Rota_CA"]    
    for rota in rotas:
        path_rotas = os.path.expanduser('~')+"/Análise_Simulações/"+DATA_HORA+"/"+rota
        os.mkdir(path_rotas)
        
    processos = ["/move_base", "/amcl", "/map_server", "/rosmaster"]
    for rota in rotas:
        for processo in processos:
            path_rotas_processos = os.path.expanduser('~')+"/Análise_Simulações/"+DATA_HORA+"/"+rota+"/"+processo
            os.mkdir(path_rotas_processos)
            
    
    if args.o == None: args.o = 1
    else: args.o = int(args.o)
    
    if args.t == "full":
        while n < int(args.n):
            try:
                time_file = open(path+"/time_file_full.txt", "x")
            except: pass
            sim_laucher(args.t, args.rv, args.gz, n, DATA_HORA)
            n = n + 1

    elif args.t == "default":
        while n < int(args.n):
            try:
                time_file = open(path+"/time_file_default.txt", "x")
            except: pass
            sim_laucher(args.t, args.rv, args.gz, n, DATA_HORA)
            n = n + 1
    
    elif args.t == "both":
        while n < int(args.n):
            try:
                time_file = open(path+"/time_file_full.txt", "x")
            except: pass
            sim_laucher("full",args.rv, args.gz, n, DATA_HORA)
            n = n + 1
        n = 0 
        while n < int(args.n):
            try:
                time_file = open(path+"/time_file_default.txt", "x")
            except: pass
            sim_laucher("default",args.rv, args.gz, n, DATA_HORA)
            n = n + 1

    print('ALL SIMULATIONS DONE!')
    
    param_file = open(os.path.expanduser('~')+'/Análise_Simulações/'+ DATA_HORA +"/Params_Simulation.txt", "x")
    param_file.write("-t tipo: "+str(args.t))
    param_file.write("\n-n número de rodadas: "+str(args.n))
    param_file.write("\n-rv rviz on/off: "+str(args.rv))
    param_file.write("\n-gz gazebo on/off: "+str(args.gz))
    param_file.write("\n-ss coloca obstáculos na sombra ou não (default false): "+str(args.ss))
    param_file.write("\n-o número de obstáculos por rota (default 1): "+str(args.o))
    param_file.write("\n-a realiza análise dos dados: "+str(args.a))
    param_file.close()
    
    path_params = os.path.expanduser('~') + "/catkin_ws/src/turtlebot3/turtlebot3_navigation/param/"
    files = [path_params + 'base_local_planner_params.yaml',
                path_params + 'costmap_common_params_burger.yaml',
                path_params + 'dwa_local_planner_params_burger.yaml',
                path_params + 'global_costmap_params.yaml',
                path_params + 'GlobalPlannerParams.yaml',
                path_params + 'local_costmap_params.yaml',
                path_params + 'move_base_params.yaml']
    
    
    for f in files:
            shutil.copy(f, os.path.expanduser('~')+'/Análise_Simulações/'+ DATA_HORA + '/Parâmetros_iniciais_TB3')
    
    
    
    if args.a == "true":
        print('STARTING ANALYSIS!')
        analise.analysis(args.t,args.n, DATA_HORA)
        print("ANALYSIS DONE!")
    