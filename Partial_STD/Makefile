
# headers:
ver    =debug

HDRS    = infra.h \
	HtkFile.h \
	Dataset.h \
	partial_DTW.h

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

all: partial_dtw_std 

partial_dtw_std:  $(OBJS) 
	$(CC) $(OBJS) $(LFLAGS) -o partial_dtw_std

%.o: %.cpp $(HDRS)
	$(CC) $(CFLAGS) -c $<


clean:
	rm -f *.o partial_dtw_std

