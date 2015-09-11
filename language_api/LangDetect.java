import java.util.ArrayList;
import com.cybozu.labs.langdetect.Detector;
import com.cybozu.labs.langdetect.DetectorFactory;
import com.cybozu.labs.langdetect.Language;
import com.cybozu.labs.langdetect.LangDetectException;
class LangDetect {
    public void init(String profileDirectory) throws LangDetectException {
        DetectorFactory.loadProfile(profileDirectory);
    }
    public String detect(String text) throws LangDetectException {
        Detector detector = DetectorFactory.create();
        detector.append(text);
        return detector.detect();
    }
    public ArrayList<Language> detectLangs(String text) throws LangDetectException {
        Detector detector = DetectorFactory.create();
        detector.append(text);
        return detector.getProbabilities();
    }

    public static void main(String [] args){
    	LangDetect ld = new LangDetect();
	try{
		ld.init(System.getProperty("user.dir")+"/profiles");
		System.out.println(ld.detect(args[0]));
	}
	catch(Exception e){
		System.out.println("en");
	}
    }
}
