import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER
import math


class MoneyConverter(toga.App):
    DENOMINATIONS = [500, 200, 100, 50, 25, 10]
    DENOMINATION_COLORS = {
        500: "#4CAF50",  # Green
        200: "#2196F3",  # Blue
        100: "#FF9800",  # Orange
        50: "#9C27B0",   # Purple
        25: "#F44336",   # Red
        10: "#795548",   # Brown
    }
    DENOMINATION_NAMES = {
        500: "500 Unit",
        200: "200 Unit",
        100: "100 Unit",
        50: "50 Unit",
        25: "25 Unit",
        10: "10 Unit",
    }

    def startup(self):
        # Create main window
        self.main_window = toga.MainWindow(title=self.formal_name, size=(400, 800))
        
        # Input section
        input_label = toga.Label(
            "Enter Amount to Convert:",
            style=Pack(padding=(0, 0, 5, 0), font_size=14, font_weight="bold")
        )
        
        self.amount_input = toga.TextInput(
            placeholder="Enter amount (e.g., 1000)",
            style=Pack(flex=1, padding=(0, 10, 0, 0))
        )
        
        self.currency_label = toga.Label(
            "Original Currency",
            style=Pack(padding=(0, 10, 0, 0), font_size=12)
        )
        
        input_box = toga.Box(
            children=[input_label],
            style=Pack(direction=COLUMN, padding=(20, 20, 10, 20))
        )
        
        input_row = toga.Box(
            children=[self.amount_input, self.currency_label],
            style=Pack(direction=ROW, padding=(0, 20, 20, 20))
        )
        
        # Convert button
        self.convert_button = toga.Button(
            "Convert & Divide by 100",
            on_press=self.convert_amount,
            style=Pack(padding=(0, 20, 20, 20), font_size=14, font_weight="bold")
        )
        
        # Results section
        results_label = toga.Label(
            "Results:",
            style=Pack(padding=(20, 20, 10, 20), font_size=16, font_weight="bold", color="#2E7D32")
        )
        
        # Original amount display
        self.original_label = toga.Label(
            "Original Amount: -",
            style=Pack(padding=(0, 20, 5, 20), font_size=12)
        )
        
        # Divided amount display
        self.divided_label = toga.Label(
            "After ÷ 100: -",
            style=Pack(padding=(0, 20, 20, 20), font_size=14, font_weight="bold", color="#1565C0")
        )
        
        # Denominations header
        denominations_header = toga.Label(
            "Currency Breakdown:",
            style=Pack(padding=(20, 20, 10, 20), font_size=14, font_weight="bold")
        )
        
        # Container for denomination displays
        self.denominations_container = toga.ScrollContainer(
            horizontal=False,
            style=Pack(flex=1, padding=(0, 20, 20, 20))
        )
        
        # Initialize denominations box
        self.denominations_box = toga.Box(style=Pack(direction=COLUMN))
        self.denominations_container.content = self.denominations_box
        
        # Create visual illustration header
        visual_header = toga.Label(
            "Visual Representation:",
            style=Pack(padding=(20, 20, 10, 20), font_size=14, font_weight="bold")
        )
        
        # Container for visual representation
        self.visual_container = toga.ScrollContainer(
            horizontal=False,
            style=Pack(flex=1, padding=(0, 20, 20, 20))
        )
        
        # Initialize visual box
        self.visual_box = toga.Box(style=Pack(direction=COLUMN, padding=10))
        self.visual_container.content = self.visual_box
        
        # Create main container with all elements
        main_container = toga.Box(
            children=[
                input_box,
                input_row,
                self.convert_button,
                results_label,
                self.original_label,
                self.divided_label,
                denominations_header,
                self.denominations_container,
                visual_header,
                self.visual_container,
            ],
            style=Pack(direction=COLUMN)
        )
        
        # Set window content
        self.main_window.content = main_container
        self.main_window.show()
    
    def convert_amount(self, widget):
        try:
            # Get and validate input
            original_amount = float(self.amount_input.value.strip())
            
            # Divide by 100
            divided_amount = original_amount / 100
            
            # Update result labels
            self.original_label.text = f"Original Amount: {original_amount:,.2f}"
            self.divided_label.text = f"After ÷ 100: {divided_amount:,.2f}"
            
            # Calculate denominations
            denominations_result = self.calculate_denominations(divided_amount)
            
            # Update denominations display
            self.update_denominations_display(denominations_result, divided_amount)
            
            # Update visual representation
            self.update_visual_representation(denominations_result)
            
        except ValueError:
            # Show error for invalid input
            self.original_label.text = "Original Amount: Invalid input!"
            self.divided_label.text = "After ÷ 100: -"
            self.clear_displays()
        except Exception as e:
            self.original_label.text = f"Error: {str(e)}"
    
    def calculate_denominations(self, amount):
        """Break amount into denominations"""
        result = {}
        remaining = amount
        
        for denom in self.DENOMINATIONS:
            if remaining >= denom:
                count = int(remaining // denom)
                result[denom] = count
                remaining = remaining - (count * denom)
                remaining = round(remaining, 2)  # Handle floating point
            else:
                result[denom] = 0
        
        # Handle remainder (if any)
        if remaining > 0:
            # Add remainder to smallest denomination or show as leftover
            smallest_denom = self.DENOMINATIONS[-1]
            result[smallest_denom] += math.ceil(remaining / smallest_denom)
        
        return result
    
    def update_denominations_display(self, denominations, total_amount):
        """Update the denominations display"""
        # Clear previous content
        self.denominations_box.children.clear()
        
        # Add total breakdown
        total_label = toga.Label(
            f"Total: {total_amount:,.2f} =",
            style=Pack(padding=(0, 0, 10, 0), font_size=12, font_style="italic")
        )
        self.denominations_box.add(total_label)
        
        # Add each denomination
        for denom in self.DENOMINATIONS:
            count = denominations.get(denom, 0)
            if count > 0:
                value = count * denom
                percentage = (value / total_amount * 100) if total_amount > 0 else 0
                
                denom_box = toga.Box(style=Pack(direction=ROW, padding=(5, 0, 5, 0)))
                
                # Color indicator
                color_box = toga.Box(style=Pack(
                    width=20,
                    height=20,
                    background_color=self.DENOMINATION_COLORS[denom],
                    padding=(0, 10, 0, 0)
                ))
                
                # Denomination info
                info_label = toga.Label(
                    f"{count} × {denom} = {value:,.2f} ({percentage:.1f}%)",
                    style=Pack(flex=1, font_size=13)
                )
                
                denom_box.add(color_box)
                denom_box.add(info_label)
                self.denominations_box.add(denom_box)
        
        # Show if no denominations needed (amount too small)
        if all(count == 0 for count in denominations.values()):
            message = toga.Label(
                "Amount is less than smallest denomination (10)",
                style=Pack(padding=10, font_size=12, color="#666")
            )
            self.denominations_box.add(message)
    
    def update_visual_representation(self, denominations):
        """Create visual representation of denominations"""
        # Clear previous content
        self.visual_box.children.clear()
        
        total_items = sum(denominations.values())
        if total_items == 0:
            message = toga.Label(
                "Amount too small to visualize",
                style=Pack(padding=20, font_size=12, color="#666", text_align=CENTER)
            )
            self.visual_box.add(message)
            return
        
        # Create visual representation
        for denom in self.DENOMINATIONS:
            count = denominations.get(denom, 0)
            if count > 0:
                # Denomination header
                header = toga.Label(
                    f"{self.DENOMINATION_NAMES[denom]} ({count} pcs):",
                    style=Pack(
                        padding=(10, 0, 5, 0),
                        font_size=12,
                        font_weight="bold",
                        color=self.DENOMINATION_COLORS[denom]
                    )
                )
                self.visual_box.add(header)
                
                # Create a row of visual blocks
                max_per_row = 10
                for i in range(0, count, max_per_row):
                    row_count = min(max_per_row, count - i)
                    
                    row_box = toga.Box(style=Pack(direction=ROW, padding=(0, 0, 5, 0)))
                    
                    for j in range(row_count):
                        # Create visual block
                        block = toga.Box(style=Pack(
                            width=25,
                            height=25,
                            background_color=self.DENOMINATION_COLORS[denom],
                            margin=(2, 2, 2, 2),
                            border_color="#333",
                            border_width=1
                        ))
                        
                        # Add value label inside block for larger denominations
                        if denom >= 100:
                            value_label = toga.Label(
                                str(denom),
                                style=Pack(
                                    font_size=8,
                                    color="white",
                                    text_align=CENTER,
                                    padding=(5, 0, 0, 0)
                                )
                            )
                            # Note: Toga doesn't support direct child labels on Box
                            # In practice, you'd create a custom widget or use a different approach
                        
                        row_box.add(block)
                    
                    self.visual_box.add(row_box)
        
        # Add summary
        summary = toga.Label(
            f"Total pieces: {total_items}",
            style=Pack(padding=(15, 0, 5, 0), font_size=11, font_style="italic")
        )
        self.visual_box.add(summary)
    
    def clear_displays(self):
        """Clear all display areas"""
        self.denominations_box.children.clear()
        self.visual_box.children.clear()


def main():
    return MoneyConverter()


if __name__ == "__main__":
    app = main()
    app.main_loop()
