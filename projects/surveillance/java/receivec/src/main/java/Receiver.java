import com.sun.net.httpserver.Headers;
import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpServer;
import org.opencv.core.Core;
import org.opencv.core.MatOfByte;
import org.opencv.imgcodecs.Imgcodecs;

import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.concurrent.Executors;
import java.util.concurrent.Semaphore;

public class Receiver {

    private static Frame threaded_frame = new Frame();
    private static final Semaphore semaphore = new Semaphore(1);

    static {
        System.loadLibrary(Core.NATIVE_LIBRARY_NAME);
    }

    private static int serverPort = 8080;

    public static void main(String[] args) throws InterruptedException, IOException {

        final Thread server = new Thread() {
            public void run() {
                try {
                    ServerSocket socket = new ServerSocket(serverPort);
                    Socket clientSocket = socket.accept();
                    final ObjectInputStream ios = new ObjectInputStream(clientSocket.getInputStream());

                    //add authentication
                    //retrieve frames only when requested by a client

                    while (true) {
                        System.out.println("Waiting to receive");

                        Frame frame = (Frame) ios.readObject();
                        Receiver.threaded_frame.setFrame(frame);

                        System.out.println("Received frame");
                        Thread.sleep(100);

                        synchronized (semaphore) {
                            semaphore.notifyAll();
                        }
                    }
                } catch (Exception ignore) {
                    ignore.printStackTrace();
                }
            }
        };

        server.start();

        Thread.sleep(1000);

        HttpServer httpServer = HttpServer.create(new InetSocketAddress(8081), 0);
        httpServer.createContext("/", new HomeHandler());
        httpServer.createContext("/streaming.mjpg", new SHandler());
        httpServer.setExecutor(Executors.newCachedThreadPool());
        httpServer.start();

        System.out.println("Started server");
        server.join();
    }

    static class HomeHandler implements HttpHandler {
        public void handle(HttpExchange t) throws IOException {
            byte[] response = "<!DOCTYPE html><html><body><img src=\"streaming.mjpg\"></body></html>".getBytes();
            t.getResponseHeaders().set("Content-Type", "text/html");
            t.sendResponseHeaders(200, response.length);
            OutputStream os = t.getResponseBody();
            os.write(response);
            os.close();
        }
    }

    static class SHandler implements HttpHandler {
        private static final String NL = "\r\n";
        private static final String BOUNDARY = "FRAME";
        private static final String HEAD = "--" + BOUNDARY + NL +
                "Content-Type: image/jpeg" + NL +
                "Content-Length: ";

        @Override
        public void handle(HttpExchange t) throws IOException {
            Headers h = t.getResponseHeaders();
            h.set("Age", "0");
            h.set("Cache-Control", "no-cache, private");
            h.set("Pragma", "no-cache");
            h.set("Content-Type", "multipart/x-mixed-replace; boundary=" + BOUNDARY);
            t.sendResponseHeaders(200, 0);
            OutputStream os = t.getResponseBody();

            while (true) {
                try {
                    synchronized (semaphore) {
                        semaphore.wait();
                    }

                    MatOfByte mat = new MatOfByte();
                    Imgcodecs.imencode(".jpg", threaded_frame.toMat(), mat);

                    os.write((HEAD + mat.toArray().length + NL + NL).getBytes());
                    os.write(mat.toArray());
                    os.write(NL.getBytes());
                    os.flush();

                } catch (InterruptedException e) {
                    e.printStackTrace();
                    os.close();
                }
            }
        }
    }
}
