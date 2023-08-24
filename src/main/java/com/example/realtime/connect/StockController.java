package com.example.realtime.connect;


import org.python.core.PyFunction;
import org.python.core.PyObject;
import org.python.util.PythonInterpreter;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/test-stock")
public class StockController {

    private static PythonInterpreter interpreter;

    @GetMapping("/get-stock")
    public String pytest(){

        interpreter = new PythonInterpreter();
        interpreter.execfile("src/main/python/df_stock.py");
        interpreter.exec("print(testStock())");

        PyFunction pyFunction = interpreter.get("testStock", PyFunction.class);
        PyObject pyobj = pyFunction.__call__();

        System.out.println(pyobj.toString());

        return pyobj.toString();
    }
}
