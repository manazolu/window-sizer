import pytest
from calculations import (
    calculate_new_width,
    calculate_new_height,
    calculate_wing,
    calculate_rope,
    calculate_net
)


class TestCalculateNewWidth:
    """Test cases for calculate_new_width function"""
    
    def test_18mm_frame(self):
        assert calculate_new_width(100, '18mm') == 70
        assert calculate_new_width(500, '18mm') == 470
        assert calculate_new_width(50, '18mm') == 20
    
    def test_25mm_frame(self):
        assert calculate_new_width(100, '25mm') == 76
        assert calculate_new_width(500, '25mm') == 476
        assert calculate_new_width(50, '25mm') == 26
    
    def test_26mm_frame(self):
        assert calculate_new_width(100, '26mm') == 60
        assert calculate_new_width(500, '26mm') == 460
        assert calculate_new_width(50, '26mm') == 10
    
    def test_18mm_flis_frame(self):
        assert calculate_new_width(100, '18mm-flis') == 38
        assert calculate_new_width(500, '18mm-flis') == 438
        assert calculate_new_width(70, '18mm-flis') == 8
    
    def test_string_input(self):
        assert calculate_new_width('100', '18mm') == 70
        assert calculate_new_width('500', '25mm') == 476
    
    def test_invalid_frame(self):
        with pytest.raises(ValueError, match="Invalid frame value"):
            calculate_new_width(100, 'invalid_frame')
        
        with pytest.raises(ValueError, match="Invalid frame value"):
            calculate_new_width(100, '30mm')


class TestCalculateNewHeight:
    """Test cases for calculate_new_height function"""
    
    def test_18mm_frame(self):
        assert calculate_new_height(200, '18mm') == 150
        assert calculate_new_height(600, '18mm') == 550
        assert calculate_new_height(80, '18mm') == 30
    
    def test_25mm_frame(self):
        assert calculate_new_height(200, '25mm') == 145
        assert calculate_new_height(600, '25mm') == 545
        assert calculate_new_height(80, '25mm') == 25
    
    def test_26mm_frame(self):
        assert calculate_new_height(200, '26mm') == 123
        assert calculate_new_height(600, '26mm') == 523
        assert calculate_new_height(100, '26mm') == 23
    
    def test_18mm_flis_frame(self):
        assert calculate_new_height(200, '18mm-flis') == 138
        assert calculate_new_height(600, '18mm-flis') == 538
        assert calculate_new_height(80, '18mm-flis') == 18
    
    def test_string_input(self):
        assert calculate_new_height('200', '18mm') == 150
        assert calculate_new_height('600', '25mm') == 545
    
    def test_invalid_frame(self):
        with pytest.raises(ValueError, match="Invalid frame value"):
            calculate_new_height(200, 'invalid_frame')


class TestCalculateWing:
    """Test cases for calculate_wing function"""
    
    def test_18mm_flis_frame(self):
        assert calculate_wing(150, '18mm-flis') == 139
        assert calculate_wing(300, '18mm-flis') == 289
        assert calculate_wing(20, '18mm-flis') == 9
    
    def test_other_frames(self):
        assert calculate_wing(150, '18mm') == 143
        assert calculate_wing(150, '25mm') == 143
        assert calculate_wing(150, '26mm') == 143
        assert calculate_wing(300, '18mm') == 293
    
    def test_string_input(self):
        assert calculate_wing('150', '18mm') == 143
        assert calculate_wing('150', '18mm-flis') == 139
    
    def test_edge_cases(self):
        assert calculate_wing(11, '18mm-flis') == 0
        assert calculate_wing(7, '18mm') == 0


class TestCalculateRope:
    """Test cases for calculate_rope function"""
    
    def test_basic_calculation(self):
        assert calculate_rope(100, 200) == 600  # (100 + 200) * 2
        assert calculate_rope(50, 75) == 250    # (50 + 75) * 2
        assert calculate_rope(300, 400) == 1400 # (300 + 400) * 2
    
    def test_string_input(self):
        assert calculate_rope('100', '200') == 600
        assert calculate_rope('50', '75') == 250
    
    def test_zero_values(self):
        assert calculate_rope(0, 100) == 200
        assert calculate_rope(100, 0) == 200
        assert calculate_rope(0, 0) == 0
    
    def test_same_dimensions(self):
        assert calculate_rope(100, 100) == 400


class TestCalculateNet:
    """Test cases for calculate_net function"""
    
    def test_18mm_frames(self):
        assert calculate_net(100, '18mm') == 50.0
        assert calculate_net(200, '18mm') == 100.0
        assert calculate_net(150, '18mm-flis') == 75.0
    
    def test_25mm_and_26mm_frames(self):
        assert calculate_net(300, '25mm') == 100.0
        assert calculate_net(300, '26mm') == 100.0
        assert calculate_net(150, '25mm') == 50.0
        assert calculate_net(150, '26mm') == 50.0
    
    def test_string_input(self):
        assert calculate_net('100', '18mm') == 50.0
        assert calculate_net('300', '25mm') == 100.0
    
    def test_invalid_frame(self):
        with pytest.raises(ValueError, match="Invalid frame value"):
            calculate_net(100, 'invalid_frame')
    
    def test_odd_numbers(self):
        # Test division behavior with odd numbers
        assert calculate_net(101, '18mm') == 50.5
        assert calculate_net(101, '25mm') == pytest.approx(33.666666666666664)


class TestIntegrationScenarios:
    """Integration tests using realistic window dimensions"""
    
    def test_typical_window_18mm(self):
        """Test typical window with 18mm frame"""
        width, height = 800, 1200
        frame = '18mm'
        
        new_width = calculate_new_width(width, frame)
        new_height = calculate_new_height(height, frame)
        wing = calculate_wing(new_height, frame)
        rope = calculate_rope(width, height)
        net = calculate_net(width, frame)
        
        assert new_width == 770
        assert new_height == 1150
        assert wing == 1143
        assert rope == 4000
        assert net == 400.0
    
    def test_typical_window_25mm(self):
        """Test typical window with 25mm frame"""
        width, height = 600, 800
        frame = '25mm'
        
        new_width = calculate_new_width(width, frame)
        new_height = calculate_new_height(height, frame)
        wing = calculate_wing(new_height, frame)
        rope = calculate_rope(width, height)
        net = calculate_net(width, frame)
        
        assert new_width == 576
        assert new_height == 745
        assert wing == 738
        assert rope == 2800
        assert net == 200.0
    
    def test_small_window_edge_case(self):
        """Test very small window dimensions"""
        width, height = 100, 150
        frame = '26mm'
        
        new_width = calculate_new_width(width, frame)
        new_height = calculate_new_height(height, frame)
        wing = calculate_wing(new_height, frame)
        rope = calculate_rope(width, height)
        net = calculate_net(width, frame)
        
        assert new_width == 60
        assert new_height == 73
        assert wing == 66
        assert rope == 500
        assert net == pytest.approx(33.333333333333336)


if __name__ == '__main__':
    pytest.main([__file__])