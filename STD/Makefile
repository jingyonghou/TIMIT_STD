
# headers:
ver    =debug

HDRS    = infra.h \
	HtkFile.h \
	Dataset.h \
	DTW.h

# sources:
SRCS    = main.cpp \
	HtkFile.cpp \
	Dataset.cpp

CC      = g++

ifeq ($(ver), debug)
	CFLAGS = -g -std=c++0x -Iinfra2 -I.
	LFLAGS = -g -std=c++0x -pthread -Linfra2 -linfra 
else
	CFLAGS = -O3 -std=c++0x -Iinfra2 -I.
	LFLAGS = -O3 -std=c++0x -pthread -Linfra2 -linfra 
endif

OBJS    = $(SRCS:.cpp=.o)

all: dtw_std 

dtw_std:  $(OBJS) 
	$(CC) $(OBJS) $(LFLAGS) -o dtw_std

%.o: %.cpp $(HDRS)
	$(CC) $(CFLAGS) -c $<


clean:
	rm -f *.o dtw_std

