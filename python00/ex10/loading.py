"""
You are about to discover the yield operator!
So let’s create a function called ft_progress(lst).
The function will display the progress of a for loop.
"""

import time

def load_bar(total,tim):
    
    progress = 0
    percentage = 0
    equalLoading = "="
    emptyLoading = ""
    cIni = "["
    cFin = "]"
    load_bar2 = cIni + emptyLoading + cFin
    load_barNew = ""
    bar_lenght = 20
    start_time = None
    
    if progress == 0 : percentage = 0
    
    for progress in range (1,total+1):
        percentage = round(progress/total*100,2)
        pr = progress/total
        num_bar = int(pr*bar_lenght)
        bar = "[" + "="* num_bar + ">>" + " " * (bar_lenght-num_bar)+"]"
        
        if start_time is None:
            start_time = time.time()
        
        elapsed_time = round(time.time() - start_time, 2)
        
        if progress == total:
            print(f"\rETA: 0s [{percentage}%] [{bar}] [{progress}/{total}] | elapsed time {elapsed_time}s", end="")
        else:
            time_remaining = round(elapsed_time / progress * (total - progress), 2)
            print(f"\rETA: {time_remaining}s [{percentage}%] [{bar}] [{progress}/{total}] | elapsed time {elapsed_time}s", end="")
        
        yield progress
        
    print("\nLoading complete.")

if __name__ == '__main__':
    tim = 0.05
    for progress in load_bar(100,tim):
        time.sleep(tim)


