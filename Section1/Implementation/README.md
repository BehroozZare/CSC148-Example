![Solar System Simulation](Figures/solar_system_simulation.gif)

# Implement a Function for a Circular Solar System Simulation

## Objective

Now that we've sketched a simple process for solving the problem defined in the [Design Section](../Design/README.md), we need to start converting those thoughts into code! Let's follow the step-by-step guide provided in the course notes.

### Step 1: Write Example Uses
We have already gone through the process in the [Design Section](../Design/README.md)! To have a simpler output instead of (66.6667, 0), we can consider the screen size to be 558 instead of 600 pixels so $558 \div 279 = 2$. Then we can simply multiply each of the distances by 2! This will turn the output to `[(62,0),(124,0),(186,0),(248,0),(372,0),(434,0),(496,0), (558,0)]`. 

### Step 2: Write the Function Header

Since we are not writing the function from scratch and we want to see the effect of our code in the solar system simulator, the function recipe is given to us!

```python
def compute_init_positions(screen_height, screen_width, solar_distances):
```

Seeing the function definition, we face the first problem. While we know what `solar_distances` is, instead of a single size for the screen, we have two sizes! This means that we did not consider that the screen is not square. Let's look back at our simulator above! We see that the last planet's distance is constrained by the height of the screen. So should we consider only the `screen_height` parameter? What if the width was smaller? Can we make our code more general with a small effort? Well, we can assume the screen size parameter in the [Design Section](../Design/README.md) as the minimum of the two sizes! So our screen size is now:

```python
screen_size = min(screen_height, screen_width)
```

### Step 3: Write the Function Description

Let's follow the tasks of writing all these things! It is hard! It is boring! But trust me, having comments, input-output checks, etc., in your code will improve your mental health in the long run! Also, embrace this boredom (quoted from [Deep Work](https://www.goodreads.com/book/show/25744928-deep-work))!

TODO by convention, our docstrings should refer to each parameter by name in the docstring when saying what the code will do. Please update this docstring wherever it appears here and in the implementation.

TODO make sure the spacing in the doctest example is consistent wherever it appears here and in the implementation.

TODO for preconditions, CSC148 documents these in the docstring and then assumes they are true in the function body instead of explicitly including assert statements. Please update this for any asserts in the code.

```python
def compute_init_positions(screen_height: int, screen_width: int, solar_distances: list) -> list[tuple]:
    """Return the initial position of each planet
    >>> compute_init_positions(558,992,[31, 31, 31, 31, 62, 31, 31, 31])
    [(62, 0), (124, 0), (186, 0), (248, 0), (372, 0), (434, 0),(496, 0), (558, 0)]
    """
```

### Step 4: Implement the Function Body

Ok, let's get real! Based on the [Design Section](../Design/README.md), the first step is:

> 1. We compute the maximum distance between the furthest planet and the sun.

Let's code this part:

```python
def compute_init_positions(screen_height: int, screen_width: int, solar_distances: list()) -> list[tuple]:
    """Return the initial position of each planet
    >>> compute_init_positions(558,992,[31, 31, 31, 31, 62, 31, 31, 31])
    [(62,0),(124,0),(186,0),(248,0),(372,0),(434,0),(496,0), (558,0)]
    """
    # Check the precondition
    assert solar_distances != []  
    assert screen_height != 0
    assert screen_width != 0

    # Compute the distance between the sun and the last planet
    furthest_planet_distance = sum(solar_distances)
```

In this example, we use the built-in `sum` function to compute the total distance between the sun and the last planet for us.

TODO replace the blurb below to comment on the preconditions we chose to include instead.

Now in this part, I chose to make the function fail when the screen is not defined properly or the distances are not given. However, when you design your code, you can choose the behavior of your function in these cases and write code to handle these appropriately. 

Let's move on to the next step mentioned in the [Design Section](../Design/README.md):

> 2. We use this distance and the screen size to scale the distances proportionally to the screen.

How can we code this? We have already seen the math as below:

$$
\frac{279}{600} = \frac{31}{x} \rightarrow \frac{600 \times 31}{279} \approx 67
$$

What are these values in our code? The 279 is already computed in the variable `furthest_planet_distance`. What is 600? It is the screen size. However, at that time our understanding of the problem was not complete as the screen is not square. So now the variable that defines 600 is `screen_size` mentioned in [Step 2](#step-2-write-the-function-header). What is 31? Well, it is one of the distances derived from the `solar_distances` list. So we are basically doing this for each entry in `solar_distances` to compute the proportional distance:

$$
 \frac{screen\_size}{furthest\_planet\_distance} \times solar\_distances[i] 
$$

Let's add this to the code!

TODO list() should be list; please check for this in all code and fix.

```python
def compute_init_positions(screen_height: int, screen_width: int, solar_distances: list()) -> list[tuple]:
    """Return the initial position of each planet
    >>> compute_init_positions(558,992,[31, 31, 31, 31, 62, 31, 31, 31])
    [(62,0),(124,0),(186,0),(248,0),(372,0),(434,0),(496,0), (558,0)]
    """

    # Check the precondition
    assert solar_distances != []
    assert screen_height != 0
    assert screen_width != 0

    # Compute the distance between the sun and the last planet
    furthest_planet_distance = sum(solar_distances)

    # Compute the screen size
    screen_size = min(screen_height, screen_width)

    # Compute the scaling factor
    scaling_factor = screen_size / furthest_planet_distance
    screen_distances = [distance * scaling_factor for distance in solar_distances]
```

TODO update the above to not use a list comprehension, but rather an accumulator pattern instead with a for-loop.

Now we are reaching the final step of our first design outline, which is:

> 3. Since the coordinates are on the horizontal line in the middle of the screen, the height is zero and the x-values are computed based on the distance of each planet to the sun.

Let's implement this! 

```python
def compute_init_positions(screen_height: int, screen_width: int, solar_distances: list()) -> list[tuple]:
    """Return the initial position of each planet
    >>> compute_init_positions(558,992,[31, 31, 31, 31, 62, 31, 31, 31])
    [(62,0),(124,0),(186,0),(248,0),(372,0),(434,0),(496,0), (558,0)]
    """

    # Check the precondition
    assert solar_distances != []
    assert screen_height != 0
    assert screen_width != 0

    # Compute the distance between the sun and the last planet
    furthest_planet_distance = sum(solar_distances)

    # Compute the screen size
    screen_size = min(screen_height, screen_width)

    # Compute the scaling factor
    scaling_factor = screen_size / furthest_planet_distance
    screen_distances = [distance * scaling_factor for distance in solar_distances]

    # Compute the distance between each planet and sun (the center)
    distance_to_sun_in_screen = 0
    init_pos = []
    for s_dist in screen_distances:
        distance_to_sun_in_screen += s_dist
        init_pos.append(distance_to_sun_in_screen, 0)

        assert distance_to_sun_in_screen <= screen_size
    
    return init_pos
```

We save the distance to the sun in the `distance_to_sun_in_screen` variable like what we sketched with pen and paper in the [Design Section](../Design/README.md). The y-axis should be zero as the sun is the center. So the `x = distance_to_sun_in_screen` and the `y = 0` and for each planet, we append this coordinate into the `init_pos` variable. Note that we also put an assert to make sure that the 'distance_to_sun_in_screen' is not violating the basic rule that we saw in [Design Section](../Design/README.md). That is, no planet should be out of the screen! Let's copy this code into [simulate.py](simulate.py) and replace the empty function.

TODO say a bit more about how you are using assert here to "sanity check your code" when developing it OR just remove this part since it maybe distracts? In some sense, asserts like this are temporary in-line tests which is something we don't do too much of in CSC148, but I am happy to have it included.

```python
def compute_init_positions(screen_height: int, screen_width: int, solar_distances: list()) -> list[tuple]:
    pass
```

By running the function, we face an error in all red! Welcome to the world of programming! If I wrote code that fully worked on the first attempt, I would be really surprised because it is very rare to write correct code on the first attempt! I suspect that you will also get this feeling somewhere in your coding journey!

![Figure Sketch](Figures/TupleError.png)

Let's analyze this error. It says `Traceback (most recent call last)`. To understand this line, in high-level explanation, Python runs the code line by line. That is, it consecutively executes the lines that you have written. However, when it reaches a function, it will simply jump to that function to execute the function code line by line. Now, the most recent call appears last in the error message. So, the error message is telling us that on line 296 of my code, it calls the function that we have written so far.

TODO as needed, update the line numbers of the stacktrace in this section to be consistent with any revisions to the code... related, we'll want to make sure that it is clear where students can find any "starter" code and the completed version of the code.

```python
# Compute the initial position of each planet
init_positions = compute_init_positions(screen_height, screen_width, solar_distances)
```

After starting to run this function, it reaches line 271 (the last blue link in the error message, which is the most recent call).

```python
        init_pos.append(distance_to_sun_in_screen, 0)
```

When the Python tries to execute this line, it fails, and the reason is written in the error.

```python
TypeError: list.append() takes exactly one argument (2 given)
```

This error says that the `append` method expects a single input, but I am providing two inputs when I am calling it in my code! Looking at the code, I can see that while I thought I was appending a tuple, it is actually considered as two inputs: `distance_to_sun_in_screen` and `0`. So I have to fix this bug by adding parentheses for creating a tuple and then adding it to the `init_pos` list. So the fixed code is:

```python
        init_pos.append((distance_to_sun_in_screen, 0))
```

Let's run the code and enjoy our solar system!

![Solar System Simulation](Figures/buggy_animation_1.gif)

Well ... we now face another hard truth! While at the beginning of the coding journey, the red error messages and squiggly red lines are hard to solve, by gaining experience, they become easier and easier to solve. However, the type of bug that comes from our understanding of the problems will stay with us, and learning to refine our understanding and redesigning the process, which results in fixing the bug (and possibly adding other bugs), will create a great programmer out of us! As a result, coding is an iterative process!

![Programming Process](Figures/CodingLoop.jpeg)

I think it is kind of like how humans learn to interact with their surroundings! Anyway, let's understand the problem better! Let's first not doubt our understanding and make sure that the code is doing what we want it to do!

Let's start with the example that we have already written! In the course notes, there are systematic ways of testing your code, which I encourage you to use as it will be more helpful in the long run. But here I like to keep things as simple as possible. So let's first use the doctest to run the function with the example that we have written!

![alt text](Figures/DoctestExample.png)

and ..

![alt text](Figures/DoctestError.png)

Well, at first glance it is a red error! But, looking closer, it seems that the implementation of our function is not the problem. The "Expected" values and the "Got" are not different! But why this error? Remember that programming languages are not smart! So, maybe the string in Expected and Got are not the same! Remember, doctest works by checking for exact string matches between the expected and actual output! So I change the doctest to this:

```Python
def compute_init_positions(screen_height: int, screen_width: int, solar_distances: list()) -> list[tuple]:
    """Return the intial position of each planet
    >>> compute_init_positions(558,992,[31, 31, 31, 31, 62, 31, 31, 31])
    [(62.0, 0), (124.0, 0), (186.0, 0), (248.0, 0), (372.0, 0), (434.0, 0), (496.0, 0), (558.0, 0)]
    """
```

And now our doctest passes! So next time that I am writing a doctest, I will make sure that the expected strings are properly formatted! So at least for our example, the code is working. But maybe it is just true for this specific example, what if we ran our function with different inputs? Let’s run the code and perform some very basic testing — let's use ```print``` function and use the variables to see what's happening step-by-step!


```Python
def compute_init_positions(screen_height: int, screen_width: int, solar_distances: list()) -> list[tuple]:
    """Return the initial position of each planet
    >>> compute_init_positions(558,992,[31, 31, 31, 31, 62, 31, 31, 31])
    [(62.0, 0), (124.0, 0), (186.0, 0), (248.0, 0), (372.0, 0), (434.0, 0), (496.0, 0), (558.0, 0)]
    """

    # Check the precondition
    assert solar_distances != []
    assert screen_height != 0
    assert screen_width != 0

    # Compute the distance between the sun and the last planet
    furthest_planet_distance = sum(solar_distances)
    print("The solar distances are", solar_distances, "- the furthest planet is at", furthest_planet_distance)
    # Compute the screen size
    screen_size = min(screen_height, screen_width)
    print("screen height", screen_height, "- screen width", screen_width,
          "- screen size", screen_size)

    # Compute the scaling factor
    scaling_factor = screen_size / furthest_planet_distance
    screen_distances = [distance * scaling_factor for distance in solar_distances]
    print("Scaler factor:", scaling_factor, "- screen distances", screen_distances)
    # Compute the distance between each planet and sun (the center)
    distance_to_sun_in_screen = 0
    init_pos = []
    for s_dist in screen_distances:
        distance_to_sun_in_screen += s_dist
        init_pos.append((distance_to_sun_in_screen, 0))

        assert distance_to_sun_in_screen <= screen_size

    print("initial positions", init_pos)
    return init_pos
```

I like to see every variable, but you can always pick and choose which variables are worth printing. Let's see the output!
```
The solar distances are [31, 31, 31, 31, 62, 31, 31, 31] - the furthest planet is at 279
screen height 720 - screen width 1280 - screen size 720
Scaler factor: 2.5806451612903225 - screen distances [80.0, 80.0, 80.0, 80.0, 160.0, 80.0, 80.0, 80.0]
initial positions [(80.0, 0), (160.0, 0), (240.0, 0), (320.0, 0), (480.0, 0), (560.0, 0), (640.0, 0), (720.0, 0)]
```

The first two lines of printing are what we expected. For the third line, we can see that the output of 80 is actually a rounding of 79.98! While it seems okay for this example, we should keep in mind that it can produce bugs for other inputs as we saw in our [Design Section](../Design/README.md). But that's a fight for another day! For now, the output of our simulator is way off, and the initial positions are not violating the screen size. So basically, the function works based on our intention! This only means one thing: we need to refine our understanding of the problem as our design itself has a problem!

Before evaluating our assumption and our solution to the problem, note how printing this many variables can be a bit hard! Especially for a relatively small function, we needed to add this many prints. To make our lives easier, we can use the debugger to see the variables. For basic use, we can mark a line of code (with the mouse, click on a line that you are interested in) as a place where the code stops and waits for our command to proceed. Then, at that point, we can see the variables that we want, without the use of prints! For example, I add the following marks or breakpoints and see how variables change.

![alt text](Figures/BreakPoints.png)

Note that based on the reasoning that we used for adding the print functions, I added a break point just before where we wanted to print each variable. Now let's start debugging with the debug button!

![alt text](Figures/DebugButton.png)

We can see that the code stops at the first break point!

![alt text](Figures/FirstBreakPoint.png)


All that is left is to see the variables that we are interested in!

![alt text](Figures/DebugOutput1.png)

While we can see screen sizes and solar_distances variable in here. However, we cannot see `furthest_planet_distance`. This is because that line of code is still not executed. So that variable is still not created. In this scenario, we can just tell the debugger to execute the code one line at a time. To do this, we can use the "Step Over" button.

![alt text](Figures/OneStep.png)

And then we have the variable that we want!

![alt text](Figures/VariableCreation.png)


Ok, let's get back to our main objective! What was wrong with our understanding? There are many different ways to approach this problem and refine our understanding. I will explain my approach. However, feel free to explore different ways of looking at this problem before reading the rest of the text. 

Looking at the simulation, while the function works as we design, the planets are going out of the screen. Which means that something about the distance that we are considering is wrong. Let's use pen and paper again to help us identify the issue.

![alt text](Figures/Frame1.jpeg)

Based on this pen and paper drawing of what we have and how we design our algorithm, we can quickly see that we assume the maximum distance from sun as the screen size. However, it is in fact half of this distance! Ok, now we understand the problem a bit better. Let's add this to our code by simply making the `screen_size` variable to be half as big as before:

```
screen_size = min(screen_height, screen_width) // 2
```

Now if we see the animation, it is still off! But, the distance between planets seems to be more accurate!

![Solar System Simulation](Figures/buggy_animation_2.gif)


Ok, what are our other options? At this point, we have limited knowledge of how the output of our function is used to position the planets around the sun. So, the first thing we can do is watch the simulation and identify other inaccuracies. We need to be more specific about what is wrong with this simulation. Here is what I observe:

1. The first orbit is too big!
2. The planets are still going off the screen!
3. The starting point for each planet is somewhere at the top of the screen!
4. The fifth planet (Jupiter) is the biggest one around the sun, but it is the fourth one here!

Based on these observations, I will start with the one I believe is quickest to check, which is number "3." Now, you may choose any other option as the starting point. That's also fine! Often, problems are interconnected, and fixing one can result in fixing others.

Let's debug number 3! Why do the planets start from the top when we set y = 0? Basically, we assume that the horizontal line that goes through the middle of the screen is y = 0, like in our conventional coordinate system as shown below.

![alt text](Figures/Coordinate.jpeg)


It seems that our understanding of `y = 0` is incorrect. The top of the screen seems to be `y = 0`. Then, what about `x = 0`? I can think of two ways to refine my understanding of this coordinate system. First, since we are using Pygame for the simulation, I can search for the coordinate documentation on Google. Here is my Google search!

![alt text](Figures/google.png)

Alternatively, you can simply return the (x, y) coordinates for every planet as (0, 0) to see where all the planets start moving. Both methods are fine. So, how can we fix our code? Let's see the coordinate system that PyGame is using!

![alt text](Figures/NewCoordinate.jpeg)

So, we need to position all our planets based on the new coordinate system. That is, `y = 0` when the (0, 0) point is in the middle, will become `y = screen_height // 2`. Similarly, `x = 0` is actually `x = screen_width // 2`. Let's update our code accordingly:

```
init_pos.append((distance_to_sun_in_screen + screen_width // 2, screen_height // 2))
```

Now let's see the output!


![alt text](Figures/solution.gif)

Congratulations! You have now successfully completed your task! But, can we share our code with other people working on this simulation project? You are giving them this code, but can they understand it? What if they want to use your code in another coordinate system instead of Pygame? That is why it is always important to document your code so that others know how to use it! There are many ways to document code, but each organization or group of people often uses specific rules to be consistent and reduce ambiguity. In this course, we use PEP-8 standard and PyTA module for checking whether we are complying to PEP-8 standards as well as given instructions for documenting our code! Let's update our code with appropriate documentation using [PyTA](../PyTA/README.md)!


