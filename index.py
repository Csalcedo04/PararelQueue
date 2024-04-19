import os
import time 
import random
import multiprocessing as mp
import threading as th
def word_gen():
    # Set the seed based on the current time

    # List of characters to choose from for generating words
    characters = 'abcdefghijklmnopqrstuvwxyz'

    text = ''
    for i in range (100):
        random.seed(time.time())
        for _ in range(1000):
            # Generate a random word of length between 3 and 8 characters
            word_length = random.randint(1, 12)
            word = ''.join(random.choice(characters) for _ in range(word_length))
            text += word + ' '
        with open(f'text{i}.txt', 'a') as output:
            output.write(text)


def delete_files():
    for i in range(100):
        try:
            os.remove(f'text{i}.txt')
        except FileNotFoundError:
            pass
    time.sleep(10)
    try:
        os.remove('hola.txt')
    except FileNotFoundError:
        pass


#serial version
def read_txt_files_in_folder(folder_path, output_file):
    files = os.listdir(folder_path)
    
    txt_files = [file for file in files if file.endswith('.txt')]
    
    with open(output_file, 'a') as output:
        for txt_file in txt_files:
            file_path = os.path.join(folder_path, txt_file)
            with open(file_path, 'r') as file:
                words = file.read().split()
                line = ''
                for word in words:
                    line += word + ' '
                    # se define que una linea es un conjunto de 16 palabras
                    if len(line.split()) == 16:
                        output.write(line.strip() + '\n')
                        line = ''
                # si hay palabras remanentes las suba así. 
                if line:
                    output.write(line.strip() + '\n')

#pararell version  
              
def producer(file_name, folder_path):
    # The producers read text from a collection of files, one per producer.
    # They insert lines of text into a single shared queue
    txt_file_path = os.path.join(folder_path, file_name)
    with open(txt_file_path, 'r', encoding='utf-8'):
        
    print()



def consumer():
    # The consumers take the lines of text and tokenize them. Tokens are “words” separated by white space. 
    # When a consumer finds a token, it writes it to a file named
    print()

def process(file):
    producer(file)
    print()

if __name__ == '__main__':
    # Example usage
    folder_path = '.'  # RECUERDA PONER PARA QUE EL USUARIO COLOQUE EL PATH
    # word_gen()
    output_file = 'hola.txt'
    files = os.listdir(folder_path)
    txt_files = [file for file in files if file.endswith('.txt')]

    print(txt_files)
    # time1 = time.perf_counter()
    # read_txt_files_in_folder(folder_path, output_file)
    # time2 = time.perf_counter()
    # print(time2-time1)
    ctx = mp.get_context('spawn')
    result_dict = ctx.Manager().dict()
    q = ctx.Queue()
    proceses =[]
    for file in txt_files:
        p = ctx.Process(target=process, args=(file))
        p.start()
        proceses.append(p)

    for i in proceses:
        i.join()

    # delete_files()