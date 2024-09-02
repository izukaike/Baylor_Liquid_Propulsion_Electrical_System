/*
Author: Izuka Ikedionwu

Description: interfaces with on board wifi antenna

Dated Created: 9/2/24
*/
#include <iostream>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <cstring>

const int PORT_NUMBER = 4;
const char* SERVER_IP = "192.168.1.215"; // Replace with your server's IP address

class client {
    public:
	client()
        { 
		std::cout <<"*client*\n";	   
	}
        int create_socket()
        {
            // Create socket
            clientSocket = socket(AF_INET, SOCK_STREAM,0);
            if (clientSocket == -1) {
                std::cerr << "Error creating socket" << std::endl;
                return 1;
            }
            return 0;
        }

        int connect_to_server(const char* ip, const int port)
        {
            // Set server address and port
            serverAddr.sin_family = AF_INET;
            serverAddr.sin_port = htons(PORT_NUMBER);
            inet_pton(AF_INET, SERVER_IP, &serverAddr.sin_addr);

            // Connect to server
            if (connect(clientSocket, (struct sockaddr*)&serverAddr, sizeof(serverAddr)) == -1) {
                std::cerr << "Error connecting to server" << std::endl;
                close(clientSocket);
                return 1;
           }


            return 0;
        } 
        int send_to_server(const char* message)
        {
            // Send message to server
            
            if (send(clientSocket, message, strlen(message), 0) == -1)
	    {
                std::cerr << "Error sending message to server" << std::endl;
      
                return 1;
            }

            std::cout << "Message sent to server: " << message << std::endl;

            return 0;
            
        }
        int* get_from_server()
        {
	    int bytes = 0;
	    while(bytes ==  0)
	    {
		 bytes = recv(clientSocket,txBuffer, sizeof(txBuffer)-1,0);
	    }
          
            if(bytes == -1)
            {
                std::cout << "add system health code here\n";
            }
            else if (bytes == -1)
            {
                std::cout << "add system health code here\n";
            }
            
            return txBuffer;
        }
	int available_data()
	{       
		//peeks into buffer without reading anything
		int peek = MSG_PEEK;
		int temp[5];
		int bytes = recv(clientSocket,temp,sizeof(txBuffer)-1,peek);
		return bytes;
	}
        ~client() {
            close(clientSocket);
	   // delete[] txBuffer;
        }
    private:
        int    clientSocket;
        struct sockaddr_in serverAddr;
        int    txBuffer[5];
};
