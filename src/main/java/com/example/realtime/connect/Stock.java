package com.example.realtime.connect;

public class Stock {

    private Long id;

    public String comp_name;

    public Long date;

    public Long volumep;

    public Long highp;

    public Long lowp;

    public Long closep;

    public Long adjclosep;


    public Stock(String comp_name){
        this.comp_name = comp_name;
        //this.volumep = volumep;
    }

    public Stock(String comp_name, Long volumep){
        this.comp_name = comp_name;
        this.volumep = volumep;
    }

    public Stock(Long volumep){
        //this.comp_name = comp_name;
        this.volumep = volumep;
    }

    public Long getHighp(){
        return highp;
    }

    public Long getLowp(){
        return lowp;
    }


    public Long getClosep(){
        return closep;
    }

    public Long getAdjclosep(){
        return adjclosep;
    }
    public Long period_price_gap(){
        return highp - lowp;
    }


}
