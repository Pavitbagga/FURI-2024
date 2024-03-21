# def peak_detection(data, time, peaks, peak_window_size=250, peak_threshold=0.3, data_threshold = 0.1):
#     window_times = time[-1*peak_window_size:]
#     window_vals = data[-1*peak_window_size:]
#     peak_window_max = max(window_vals)
#     peak_window_max_idx = window_vals.index(peak_window_max)
#     peak_time = window_times[peak_window_max_idx]
#     if (peak_window_max > window_vals[0] + peak_threshold) and (peak_window_max > window_vals[-1] + peak_threshold): # If the peak value is greater than first value and lower than last value
#         if data[peak_window_max_idx] > data_threshold: # Filter for small movements
#             return peak_time

# peak_time = peak_detection(processed_values[5], timestamps, peaks=start_times, peak_threshold=0.2)
# if (peak_time not in start_times) and (peak_time != None):
#     start_times.append(peak_time)
#     timeout_enable = True
#     print("Detection")