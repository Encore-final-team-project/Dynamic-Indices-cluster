package com.example.realtime.connect;


import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Repository;

@Repository
public class StockRepository {

    private static JdbcTemplate jdbcTemplate;

    public StockRepository(JdbcTemplate jdbcTemplate) {
    }

    public void JdbcTemplateStationDao(JdbcTemplate jdbcTemplate) {
        this.jdbcTemplate = jdbcTemplate;
    }

    public static void save(Stock station) {
        String sql = "insert into realtime_stock (realtime_stock) values (?)";
        jdbcTemplate.update(sql, station.period_price_gap());
    }

}
