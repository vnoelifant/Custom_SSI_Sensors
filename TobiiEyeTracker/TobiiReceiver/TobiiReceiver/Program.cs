using System;
using System.Text;
using System.Net;
using System.Net.Sockets;
using Tobii.Interaction;

namespace TobiiReceiver
{
    class Program
    {
        // Main Method 
        static void Main(string[] args)
        {
            ExecuteServer();
        }

        public static void ExecuteServer()
        {
            IPHostEntry ipHost = Dns.GetHostEntry(Dns.GetHostName());
            Console.WriteLine(ipHost);
            //IPAddress ipAddr = ipHost.AddressList[0];
            IPAddress ipAddr = System.Net.IPAddress.Parse("127.0.0.1");
            Console.WriteLine(ipAddr.ToString());
            IPEndPoint localEndPoint = new IPEndPoint(ipAddr, 5555);
            
            Socket listener = new Socket(ipAddr.AddressFamily,
                         SocketType.Stream, ProtocolType.Tcp);

            Socket clientSocket = null;

            try
            {
                listener.Bind(localEndPoint);
                listener.Listen(1);

                while (true)
                {
                    Console.WriteLine("Waiting connection ... ");
                    clientSocket = listener.Accept();
                    Console.WriteLine("A client has connected");

                    Console.WriteLine("Initializing gaze streams");

                    var host = new Host();

                    var gazePointDataStream = host.Streams.CreateGazePointDataStream();

                    gazePointDataStream.GazePoint((x, y, tx) =>
                    {
                        String toSend = x.ToString() + "," + y.ToString() + "," + tx.ToString();

                        if(toSend.Length > 44)
                        {
                            toSend = toSend.Substring(0, 44) + ",";
                            byte[] gazeData = Encoding.ASCII.GetBytes(toSend);
                            //Console.WriteLine(gazeData.Length);
                            int byteSent = clientSocket.Send(gazeData);
                            Console.WriteLine(toSend.Substring(0, toSend.Length-1));
                        }
                       
                    });
                }
            }

            catch (Exception e)
            {
                Console.WriteLine(e.ToString());
            }

            clientSocket.Shutdown(SocketShutdown.Both);
            clientSocket.Close();
        }
    }
}
