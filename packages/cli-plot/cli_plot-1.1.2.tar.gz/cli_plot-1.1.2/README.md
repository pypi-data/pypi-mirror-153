# CLI Plot

A commandline app for parsing and plotting text data files.

## Installation

### Using Pip

```bash
  $ pip install cli-plot
```

### Manual

```bash
  $ git clone https://github.com/John-Lee-Cooper/cli_plot
  $ cd cli_plot
  $ python setup.py install
```

## Usage

```bash
$ cli_plot --version
$ cli_plot --help
```

### Generate demo

Generate and display some sample data, written to demo.dat

```bash
$ cli_plot --demo
```
![cli-plot](https://github.com/John-Lee-Cooper/cli_plot/raw/master/image/plot1.png)

### User Interface

 Key    | Result
 :---:  | :---  
 g      | Toggle Grid
 t      | Cycle Plot Type
 m      | Toggle Series Markers
 1-9    | Toggle Series 1-9 Display
 enter  | Save Plot to png Image
 escape | Exit

Holding the left mouse button down and moving the mouse will pan the plot.  
Rolling the mouse wheel up and down will zoom out and in where the mouse is.


### Display head of file
```bash
$ cli_plot demo.dat --type=head
```

### Plot specific columns

Plot sin and growth against time:

```bash
$ cli_plot demo.dat time sin damp
```
![cli-plot](https://github.com/John-Lee-Cooper/cli_plot/raw/master/image/plot2.png)

### Plot pairs of columns

Plot columns 2 against column 1 and column 4 against column 3:

```bash
$ cli_plot demo.dat 2,3 1,4
```
![cli-plot](https://github.com/John-Lee-Cooper/cli_plot/raw/master/image/plot3.png)

### Specify plot type

Plot data as a scatter plot:

```bash
$ cli_plot demo.dat --type=scatter
```
![cli-plot](https://github.com/John-Lee-Cooper/cli_plot/raw/master/image/plot4.png)


## Todo

## Written by

John Lee Cooper  
john.lee.cooper@gatech.edu
