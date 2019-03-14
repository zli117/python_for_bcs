import math
import random
import turtle

'''
    Comment this code so that you understand it.
    Play around with different numbers of vehicles and heat sources.
    Play with the vehicles' speed and movement parameters
    See what happens and describe your observations.
    What are some deep insights about behavior that you can draw from even 
    this simple simulation?
'''


class HeatSource(turtle.Turtle):

    def __init__(self):
        """
        Constructor of HeatSource with no argument
        """
        turtle.Turtle.__init__(self, visible=False)
        # The shape of heat source is circle
        self.shape('circle')
        # Doesn't draw anything
        self.penup()
        # Color is this
        self.color(255, 190, 60)
        # Set at a random location
        self.goto(random.randint(-200, 200), random.randint(-200, 200))
        # Make it visible
        self.showturtle()


class Vehicle2(turtle.Turtle):

    def __init__(self, input_list, vehicle_id, vehicle_type):
        """
        Construct a vehicle
        :param input_list: A list of heat sources
        :param vehicle_id: The ID of this vehicle
        :param vehicle_type: The type of the vehicle
        """
        # Base class constructor
        turtle.Turtle.__init__(self, visible=False)
        # Save to attributes
        self.vehicle_id = vehicle_id
        self.vehicle_type = vehicle_type
        self.input_list = input_list
        self.create_vehicle()
        # Parameters for calculating speed
        self.speed_parameters = [20, 0.5, 1]
        # Parameters for computing the
        self.turn_parameters = [20]
        self.moves = 0

    def create_vehicle(self):
        self.shape('turtle')
        # Set size of turtle to 1
        self.turtlesize(1)
        # Do not draw
        self.penup()
        # Special color for crossed connections
        if self.vehicle_type == 'crossed':
            self.color(random.randint(0, 150), random.randint(0, 150), 255)
        else:
            self.color(255, random.randint(0, 150), random.randint(0, 150))
        # Move to a random location
        self.goto(random.randint(-290, 290), random.randint(-290, 290))
        # Turn turtle by a random amount
        self.right(random.randint(0, 360))
        # Draw on move
        self.pendown()
        # Make visible
        self.showturtle()

    def get_input_information(self, position):
        input_distance = self.distance(position)
        input_angle = self.heading() - self.towards(position)
        return input_distance, input_angle

    def get_sensor_distances(self, distance, angle):
        sin_angle = math.sin(math.radians(angle))
        left_distance = distance - sin_angle
        right_distance = distance + sin_angle
        return left_distance, right_distance

    def compute_speed(self, left_distance, right_distance):
        if self.vehicle_type == 'crossed':
            left_speed = (self.speed_parameters[0] / (
                    right_distance ** self.speed_parameters[1])) - \
                         self.speed_parameters[2]
            right_speed = (self.speed_parameters[0] / (
                    left_distance ** self.speed_parameters[1])) - \
                          self.speed_parameters[2]
        else:
            left_speed = (self.speed_parameters[0] / (
                    left_distance ** self.speed_parameters[1])) - \
                         self.speed_parameters[2]
            right_speed = (self.speed_parameters[0] / (
                    right_distance ** self.speed_parameters[1])) - \
                          self.speed_parameters[2]
        combined_speed = (left_speed + right_speed) / 2
        return left_speed, right_speed, combined_speed

    def compute_turn_amount(self, left_speed, right_speed):
        turn_amount = self.turn_parameters[0] * (right_speed - left_speed)
        return turn_amount

    def move(self):
        combined_speed = 0
        combined_turn_amount = 0

        for current_input in self.input_list:
            input_distance, input_angle = self.get_input_information(
                current_input.position())
            left_distance, right_distance = self.get_sensor_distances(
                input_distance, input_angle)
            left_speed, right_speed, average_speed = self.compute_speed(
                left_distance, right_distance)
            turn_amount = self.compute_turn_amount(left_speed, right_speed)
            combined_turn_amount += turn_amount
            combined_speed += average_speed

        try:
            self.right(combined_turn_amount)
        except:
            print(combined_turn_amount)
        self.forward(combined_speed)
        self.moves += 1


def create_screen():
    wn = turtle.Screen()
    wn.colormode(255)
    wn.setup(1200, 800)
    wn.title("Vehicle 2")
    wn.tracer(0, 0)
    return wn


def main():
    wn = create_screen()
    num_vehicles = 5
    num_heat_sources = 6

    vehicle_list = []
    input_list = []

    for i in range(num_heat_sources):
        input_list.append(HeatSource())

    for i in range(num_vehicles):
        vehicle_list.append(
            Vehicle2(input_list, i, random.choice(["crossed", "direct"])))

    wn.update()
    while True:
        for j in range(num_vehicles):
            vehicle_list[j].move()
        wn.update()


if __name__ == '__main__':
    main()