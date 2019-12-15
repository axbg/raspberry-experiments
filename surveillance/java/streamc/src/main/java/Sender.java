import lombok.Data;

@Data
class Sender {
    private final String serverIp;
    private final int serverPort;

    private Frame frame = new Frame();

}
