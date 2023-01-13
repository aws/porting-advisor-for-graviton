package com.amazonaws.labs.GravitonReadyAssessor;

import lombok.NonNull;

import java.io.OutputStream;
import java.util.Properties;
import java.util.logging.*;

/**
 * A simple unbuffered logger that simply prints each log line as-is to standard output (System.out).
 */
public class SimpleLogger {
    private static Logger logger;
    private static Handler handler;

    static {
        Properties logProps = System.getProperties();
        logProps.setProperty("java.util.logging.SimpleFormatter.format", "%5$s%n");
        System.setProperties(logProps);
    }

    /**
     * Obtain the singleton Logger instance.
     *
     * @return The logger instance
     * @throws SecurityException
     */
    public static Logger getLogger() throws SecurityException {
        if (logger != null) {
            return logger;
        }
        logger = Logger.getLogger(SimpleLogger.class.toString());
        logger.setUseParentHandlers(false);
        handler = getAutoFlushingStreamHandler(System.out, new SimpleFormatter());
        logger.addHandler(handler);
        return logger;
    }

    /**
     * Sets the lowest log level that this logger will emit. Logs with a level lower than
     * this will be omitted from the output.
     *
     * @param level The log level
     */
    public static void setLevel(@NonNull Level level) {
        if (logger == null) getLogger();
        handler.setLevel(level);
        logger.setLevel(level);
    }

    /**
     * Returns a StreamHandler that flushes after every publish() invocation.
     * @param o the OutputStream passed to the StreamHandler constructor
     * @param f the Formatter passed to the StreamHandler constructor
     * @return
     */
    private static StreamHandler getAutoFlushingStreamHandler(@NonNull OutputStream o, @NonNull Formatter f) {
        return new StreamHandler(o, f) {
            @Override
            public synchronized void publish(@NonNull final LogRecord record) {
                super.publish(record);
                flush();
            }
        };
    }
}
