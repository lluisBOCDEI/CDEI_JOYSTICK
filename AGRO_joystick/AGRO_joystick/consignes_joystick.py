import rclpy
from rclpy.node import Node
import geometry_msgs
import sensor_msgs
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist

class Node_consignes_joystic (Node):
    def __init__(self):
        super().__init__("Node_consignes")
        self.subscription = self.create_subscription(Joy,'/joy',self.joy_callback,10)
        self.publisher = self.create_publisher(Twist,'/cmd_vel',10)

    def joy_callback(self,recieved_msg):
        #Aquesta funció es crida quan es rep un missatge del topic
        #self.get_logger().info(f'Recieved from /joy: {recieved_msg}')
        consigna_msg = Twist()
        speed_multiplier = 1.0
        turbo_speed_multiplier = 1.5

        #Es guarda la informació rellevant de comandament
        #Els missatges del comandament són 10 botons i 7 eixos. 
        if len(recieved_msg.axes) > 1:
            velocitat_x_comandament = recieved_msg.axes[0] #Joystick_esquerre amunt/avall (1/-1)
            velocitat_y_comandament = recieved_msg.axes[1] #Joystick_esquerre dreta esquerra (-1/1)
            omega_comandament = recieved_msg.axes[4] #Joystick dret dreta/esquerra (-1/1)
        else:
            velocitat_x_comandament = 0.0 #Joystick_esquerre amunt/avall (1/-1)
            velocitat_y_comandament = 0.0 #Joystick_esquerre dreta esquerra (-1/1)
            omega_comandament = 0.0 #Joystick dret dreta/esquerra (-1/1)

        if len(recieved_msg.buttons) > 1: #Botó A
            modo_turbo_on = recieved_msg.buttons[0] #Botó A
            frenada_on = recieved_msg.buttons[2] #Botó B
        else:
            modo_turbo_on = 0.0 #Botó A
            frenada_on = 0.0 #Botó B
        
        #Es processa la inforació del comandament
        consigna_msg.linear.x = speed_multiplier * velocitat_x_comandament
        consigna_msg.linear.y = speed_multiplier * velocitat_y_comandament
        consigna_msg.linear.z = 0.0

        consigna_msg.angular.x = 0.0
        consigna_msg.angular.y = 0.0
        consigna_msg.angular.z = speed_multiplier * omega_comandament
        
        #Si hi ha mode turbo, es canvien les velocitats:
        if(modo_turbo_on):
           consigna_msg.linear.x = turbo_speed_multiplier * velocitat_x_comandament
           consigna_msg.linear.y = turbo_speed_multiplier * velocitat_y_comandament
           consigna_msg.linear.z = 0.0

           consigna_msg.angular.x = 0.0
           consigna_msg.angular.y = 0.0
           consigna_msg.angular.z = turbo_speed_multiplier * omega_comandament 
           
        #Si hi ha mode fre, es canvien les velocitats a 0:
        if(frenada_on):
           consigna_msg.linear.x = turbo_speed_multiplier * velocitat_x_comandament
           consigna_msg.linear.y = turbo_speed_multiplier * velocitat_y_comandament
           consigna_msg.linear.z = 0.0

           consigna_msg.angular.x = 0.0
           consigna_msg.angular.y = 0.0
           consigna_msg.angular.z = turbo_speed_multiplier * omega_comandament

        #S'envia la info del comandament:
        #self.get_logger().info(f'Sent to /cmd_vel: {consigna_msg}')
        self.publisher.publish(consigna_msg)        


def main(args=None):
    rclpy.init()

    #Create node: Al main s'ha d crear una instància al node que has creat:

    node_consignes_inst = Node_consignes_joystic()

    #Use node: NPI pero s'ha de posar:
    rclpy.spin(node_consignes_inst)

    #Destroy node
    node_consignes_inst.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()