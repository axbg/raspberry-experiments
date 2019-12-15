import org.opencv.core.Core;
import org.opencv.core.Mat;
import org.opencv.videoio.VideoCapture;

import java.io.ObjectOutputStream;
import java.net.Socket;

import static java.lang.System.exit;

public class Main {

    private static Frame serializableFrame = new Frame();

    static {
        System.loadLibrary(Core.NATIVE_LIBRARY_NAME);
    }

    public static void main(String[] args) throws InterruptedException {
        final Sender sender = new Sender("localhost", 8080);
        final VideoCapture cam = new VideoCapture(0);
        final Mat frame = new Mat();

        if (!cam.isOpened()) {
            System.out.println("Camera couldn't be opened");
            exit(1);
        }

        Thread collectorThread = new Thread() {
            public void run() {
                try {
                    while (true) {
                        if (cam.read(frame)) {
                            serializableFrame = new Frame(frame);
                            serializableFrame.setInit(true);
                            Thread.sleep(100);
                        }
                    }
                } catch (Exception ignored) {
                    ignored.printStackTrace();
                }
            }
        };
        collectorThread.start();
        Thread.sleep(1000);

        Thread senderThread = new Thread() {
            public void run() {
                try {
                    Socket socket = new Socket(sender.getServerIp(), sender.getServerPort());
                    final ObjectOutputStream oos = new ObjectOutputStream(socket.getOutputStream());
                    while (true) {
                        if (serializableFrame.isInit()) {
                            System.out.println("Preparing to send");
                            oos.writeObject(serializableFrame);
                            oos.flush();
                            System.out.println("Sent");
                        }
                        Thread.sleep(100);
                    }
                } catch (Exception ignored) {
                    ignored.printStackTrace();
                }
            }
        };
        senderThread.start();

        System.out.println("Collector client started");
        System.out.println("Preparing to join threads");

        senderThread.join();
        collectorThread.join();
        exit(0);
    }
}
