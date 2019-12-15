import lombok.Data;
import org.opencv.core.Mat;

import java.io.Serializable;

@Data
class Frame implements Serializable {

    private byte[] frame;
    private int rows;
    private int cols;
    private int type;
    private boolean init = false;

    Frame() {
        this.frame = new byte[5000];
    }

    Frame(Mat mat) {
        byte[] byteArr = new byte[(int) (mat.total() * mat.elemSize())];
        mat.get(0, 0, byteArr);

        this.frame = byteArr;
        this.rows = mat.rows();
        this.cols = mat.cols();
        this.type = mat.type();
    }

    void setFrame(Frame frame) {
        this.frame = frame.frame;
        this.rows = frame.rows;
        this.cols = frame.cols;
        this.type = frame.type;
    }

    Mat toMat() {
        Mat mat = new Mat(this.rows, this.cols, this.type);
        mat.put(0, 0, this.frame);
        return mat;
    }
}
