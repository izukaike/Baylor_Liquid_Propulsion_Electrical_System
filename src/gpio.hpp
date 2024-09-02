#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <unistd.h> // For usleep()

class GPIO {
public:
    void init(int gpio_pin);
    ~GPIO();

    void export_gpio();
    void set_direction(bool output);
    void set_value(bool value);
	
private:
    std::string gpio_base_path_;
    int gpio_pin_;
};

void GPIO::init(int gpio_pin)
{
    // Export GPIO pin
    gpio_pin_ = gpio_pin;
    gpio_base_path_ = "/sys/class/gpio/";
    export_gpio();
}

GPIO::~GPIO()
{
    // Unexport GPIO pin
    std::ofstream unexport_file(gpio_base_path_ + "unexport");
    if (unexport_file.is_open())
    {
        unexport_file << gpio_pin_;
        unexport_file.close();
    }
}

void GPIO::export_gpio()
{
    std::ofstream export_file(gpio_base_path_ + "export");
    if (export_file.is_open())
    {
        export_file << gpio_pin_;
        export_file.close();
    } else
    {
        std::cerr << "Unable to export GPIO " << gpio_pin_ << std::endl;
    }
}

void GPIO::set_direction(bool output)
{
    std::string direction = output ? "out" : "in";
    std::ofstream direction_file(gpio_base_path_ + "gpio" + std::to_string(gpio_pin_) + "/direction");
    if (direction_file.is_open())
    {
        direction_file << direction;
        direction_file.close();
    } else
    {
        std::cerr << "Unable to set direction for GPIO " << gpio_pin_ << std::endl;
    }
}

void GPIO::set_value(bool value)
{
    std::ofstream value_file(gpio_base_path_ + "gpio" + std::to_string(gpio_pin_) + "/value");
    if (value_file.is_open()) {
        value_file << (value ? "1" : "0");
        value_file.close();
    } else {
        std::cerr << "Unable to set value for GPIO " << gpio_pin_ << std::endl;    }
}
