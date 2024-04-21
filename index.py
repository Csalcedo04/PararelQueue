import os
import time 
import random
import threading as th
from queue import Queue
import filecmp
# import multiprocessing as mp
# from multiprocessing.pool import ThreadPool


#verifica que la ruta sea un directorio
def es_directorio(ruta):
    return os.path.isdir(ruta)


#serial version
def serial_produccer( q:Queue, folder_path:str )->None:

    with open(folder_path, 'r', encoding='utf-8') as output:
        for line in output:
            q.put(line)


def serial_consumer(q:Queue, output_file:str)->None:
    unique_words = []  
    while not q.empty():
        line = q.get()
        tokens = line.split()
        if tokens != []:
            for token in tokens:
                if token not in unique_words: 
                    unique_words.append(token)  
                else:
                    pass
    with open(output_file, 'a') as output:
        output.write(str(unique_words))


def serial(q:Queue, folder_path:str , output_file:str)->None:
    files = os.listdir(folder_path)
    txt_files = [file for file in files if file.endswith('.txt')]
    if txt_files == []:
        print("No .txt files in this directory")
    else:
        for file in txt_files:
            file_path = os.path.join(folder_path, file)
            serial_produccer(q,file_path)
        serial_consumer(q, output_file)
  

#Threads
def threads_producer(q:Queue, folder_path:str)->None:
    # The producers read text from a collection of files, one per producer.
    # They insert lines of text into a single shared queue
    with open(folder_path, 'r', encoding='utf-8') as output:
       for line in output:
           q.put(line)


def threads_consumer(q:Queue, output_file:str,unique_words:list,mutex:th.Lock )->None:
    unique_words=[]
    while not q.empty(): 
        line = q.get()
        tokens = line.split()
        if tokens != []:
            for token in tokens:
                if token not in unique_words: 
                    unique_words.append(token)  
                else:
                    pass
                
    with open(output_file, 'a') as output:
        with mutex:
            output.write(str(unique_words))


def threadss(q:Queue,folder_path,output_file, mutex:th.Lock):
    files = os.listdir(folder_path)
    threads =[] 
    txt_files = [file for file in files if file.endswith('.txt')]
    unique_words = []
    if txt_files == []:
        print("No .txt files in this directory")
    else:
        for file in txt_files:
            file_path = os.path.join(folder_path, file)
            t = th.Thread(target=threads_producer, args=(q,file_path))
            t.start()
            threads.append(t)
        for i in threads:
            i.join()    
        th.Thread(target=threads_consumer, args=(q,output_file,unique_words, mutex)).start()
    
#POOL
"""No muestra mejorias con respecto al hecho con threads, es más, es significativamente más lento"""
# def pool_producer(q:Queue, folder_path:str)->None:
#     # The producers read text from a collection of files, one per producer.
#     # They insert lines of text into a single shared queue
#     with open(folder_path, 'r', encoding='utf-8') as output:
#        for line in output:
#            q.put(line)


# def pool_consumer(q:Queue, output_file:str,unique_words:list,mutex:th.Lock )->None:
#     unique_words=[]
#     while not q.empty(): 
#         line = q.get()
#         tokens = line.split()
#         if tokens != []:
#             for token in tokens:
#                 if token not in unique_words: 
#                     unique_words.append(token)  
#                 else:
#                     pass
                
#     with open(output_file, 'a') as output:
#         with mutex:
#             output.write(str(unique_words))


# def pool(q:Queue,folder_path:str,output_file:str, mutex:th.Lock)->None:
#     files = os.listdir(folder_path)
    
#     unique_words = []
#     txt_files = [file for file in files if file.endswith('.txt')]
#     if txt_files == []:
#         print("No .txt files in directory")
#     else:
#         with ThreadPool(os.cpu_count()//2) as pool:
#             # start consumer tasks
#             _ = [pool.apply_async(pool_producer, args=(q, file_path,)) for file_path in [os.path.join(folder_path, file) for file in txt_files]]
#             # wait for all tasks to complete
#             pool.close()
#             pool.join()
#         th.Thread(target=threads_consumer, args=(q,output_file,unique_words, mutex)).start()

#Process

"""La ejecuccion en procesos es muy lenta bajo las restricciones del problema, y la naturaleza de las 
colas en multiprocessing"""
# def process_producer(q:mp.Queue, folder_path:str)->None:
#     # The producers read text from a collection of files, one per producer.
#     # They insert lines of text into a single shared queue
#     with open(folder_path, 'r', encoding='utf-8') as output:
#        for line in output:
#            q.put(line)


# def process_consumer(q:mp.Queue, output_file:str,unique_words:list,mutex:mp.Lock )->None:
#     unique_words=[]
#     while not q.empty(): 
#         line = q.get()
#         tokens = line.split()
#         if tokens != []:
#             for token in tokens:
#                 if token not in unique_words: 
#                     unique_words.append(token)  
#                 else:
#                     pass
                
#     with open(output_file, 'a') as output:
#         with mutex:
#             output.write(str(unique_words)) 

if __name__ == '__main__':
    # Example usage
    while True:
        folder_path = input("Dijite un directorio con archivos .txt: ")
        if es_directorio(folder_path) == True:
            break
        else:
            print("El input digitado no es un directorio, por favor digite un directorio")
            pass

    mutex = th.Lock()

    # folder_path = 'C:/Users/salce/Documents/universidad/Comp.paralelo/rp11/tests'  # RECUERDA PONER PARA QUE EL USUARIO COLOQUE EL PATH

    #serial
    output_file = 'Carlos_output.txt'
    q = Queue()   
    time1 = time.perf_counter()
    serial(q,folder_path,output_file)
    time2 = time.perf_counter()
    print(f"serial time: {time2-time1}")

    #Threads
    output_file_t = 'Carlos_output_t.txt'
    time_t1 = time.perf_counter()
    threadss(q,folder_path,output_file_t,mutex)
    time_t2 = time.perf_counter()
    print(f"Threads time: {time_t2-time_t1}")

    #pool
    # output_file_tp = 'Carlos_output_tp.txt'
    # time_tp1 = time.perf_counter()
    # pool(q,folder_path,output_file_tp,mutex)
    # time_tp2 = time.perf_counter()
    # print(f"Threads Pool time: {time_tp2-time_tp1}")

    #Process
    # output_file_p = 'Carlos_output_p.txt'
    # pmutex = mp.Lock()
    # files = os.listdir(folder_path)
    # txt_files = [file for file in files if file.endswith('.txt')]
    # if txt_files == []:
    #     print("No .txt files in directory")
    # else:
    #     ctx = mp.get_context('spawn')
    #     unique_words = ctx.Manager().dict()
    #     qp = ctx.Queue()
    #     proceses =[]
    #     time_p1 = time.perf_counter()
    #     for file in txt_files:
    #         file_path = os.path.join(folder_path, file)
    #         p = ctx.Process(target=process_producer, args=(qp,file_path))
    #         p.start()
    #         proceses.append(p)

    #     for i in proceses:
    #         i.join()
    #     p2 = ctx.Process(target=process_consumer, args=(qp,output_file_p,unique_words,pmutex)).start()
    #     time_p2 = time.perf_counter()
    # print(f"process time: {time_p2-time_p1}")  

    #Comprobacion del contenido de los archivos output
    time.sleep(1)
    try:
        are_equals = filecmp.cmp('./'+output_file, './'+output_file_t)
        if are_equals:
            print(f"Los resultados entre {'./'+output_file} y {'./'+output_file_t} son iguales")
        else:
            print(f"Los resultados entre {'./'+output_file} y {'./'+output_file_t} son diferentes")
    except FileNotFoundError:
        pass


