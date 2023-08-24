//package com.example.realtime;
//
//
//import com.example.realtime.connect.Stock;
//import com.example.realtime.connect.StockRepository;
//import org.junit.jupiter.api.DisplayName;
//import org.junit.jupiter.api.Test;
//import org.springframework.beans.factory.annotation.Autowired;
//import org.springframework.boot.test.autoconfigure.jdbc.JdbcTest;
//import org.springframework.jdbc.core.JdbcTemplate;
//
//@JdbcTest
//public class repoTest {
//
//    private final StockRepository repo;
//
//    @Autowired
//    public repoTest(JdbcTemplate jdbcTemplate) {
//        this.repo = new StockRepository(jdbcTemplate);
//    }
//
//    @DisplayName("batch 사용하지 않고 저장한다.")
//    @Test
//    void batch_사용하지_않고_저장한다() {
//        long start = System.currentTimeMillis();
//
//        for (int i = 0; i < 10000; i++) {
//            String name = String.valueOf(i);
//            Long volume = Long.valueOf(String.valueOf(i));
//            StockRepository.save(new Stock(name,volume));
//        }
//
//        long end = System.currentTimeMillis();
//        System.out.println("수행시간: " + (end - start) + " ms");
//    }
//
//
//
//}
